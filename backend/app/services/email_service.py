import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Iterable, Union

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from app.core.config import settings

logger = logging.getLogger("gumba.email")

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates" / "emails"

_jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


class EmailService:
    """
    Single place responsible for all outgoing email in the app.

    Business-logic services (DonationService, AgentApplicationService,
    ...) call this AFTER their own DB transaction has committed. This
    class never touches the database, and send_email()/
    send_templated_email() never raise - an SMTP failure is logged
    and swallowed so it can never roll back or crash a request whose
    actual work (the approval, the status change, ...) already
    succeeded.
    """

    # -------------------------------------------------
    # TEMPLATES
    # -------------------------------------------------

    @staticmethod
    def render_template(template_name: str, context: dict) -> str:
        """
        Renders an HTML file from app/templates/emails/<template_name>.

        Raises TemplateNotFound / jinja2 errors if the template is
        missing or broken - that's a developer-time mistake (wrong
        filename, bad template syntax), not something to hide.
        Callers that want failures swallowed should use
        send_templated_email() instead of calling this directly.
        """
        template = _jinja_env.get_template(template_name)
        return template.render(**context)

    # -------------------------------------------------
    # SENDING
    # -------------------------------------------------

    @staticmethod
    def send_email(
        to: Union[str, Iterable[str]],
        subject: str,
        html_body: str,
    ) -> bool:
        """
        Sends one HTML email to one or more recipients.

        Returns True if the message was handed off to the SMTP
        server successfully, False otherwise. Never raises.
        """
        recipients = [to] if isinstance(to, str) else list(to)
        recipients = [r for r in recipients if r]

        if not recipients:
            logger.warning(
                "send_email called with no recipients (subject=%r) - "
                "skipping.",
                subject,
            )
            return False

        if not settings.MAIL_ENABLED:
            logger.warning(
                "Email is not configured (MAIL_HOST/MAIL_USERNAME/"
                "MAIL_PASSWORD missing in .env) - skipping email "
                "(subject=%r, to=%s).",
                subject,
                recipients,
            )
            return False

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = (
            f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
        )
        message["To"] = ", ".join(recipients)
        message.attach(MIMEText(html_body, "html"))

        try:
            if settings.MAIL_PORT == 465:
                # Implicit TLS from the start of the connection.
                with smtplib.SMTP_SSL(
                    settings.MAIL_HOST,
                    settings.MAIL_PORT,
                    timeout=10,
                ) as server:
                    server.login(
                        settings.MAIL_USERNAME,
                        settings.MAIL_PASSWORD,
                    )
                    server.sendmail(
                        settings.MAIL_FROM,
                        recipients,
                        message.as_string(),
                    )
            else:
                # Plain connection upgraded via STARTTLS (587, the
                # common default for most providers).
                with smtplib.SMTP(
                    settings.MAIL_HOST,
                    settings.MAIL_PORT,
                    timeout=10,
                ) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(
                        settings.MAIL_USERNAME,
                        settings.MAIL_PASSWORD,
                    )
                    server.sendmail(
                        settings.MAIL_FROM,
                        recipients,
                        message.as_string(),
                    )
        except Exception:
            logger.exception(
                "Failed to send email (subject=%r, to=%s)",
                subject,
                recipients,
            )
            return False

        logger.info(
            "Email sent (subject=%r, to=%s)",
            subject,
            recipients,
        )
        return True

    @staticmethod
    def send_templated_email(
        to: Union[str, Iterable[str]],
        subject: str,
        template_name: str,
        context: dict,
    ) -> bool:
        """
        Convenience wrapper: render a template, then send it.

        Unlike render_template(), this never raises - a bad/missing
        template is logged and treated as a failed send, for the
        same "never break the caller" reason as send_email().
        """
        try:
            html_body = EmailService.render_template(
                template_name, context
            )
        except TemplateNotFound:
            logger.exception(
                "Email template not found: %s (subject=%r)",
                template_name,
                subject,
            )
            return False
        except Exception:
            logger.exception(
                "Failed to render email template: %s (subject=%r)",
                template_name,
                subject,
            )
            return False

        return EmailService.send_email(to, subject, html_body)