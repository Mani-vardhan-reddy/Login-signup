from app.models.signup_models import Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.util_functions.email_service import smtp_service

class CommonServices():
    
    def render_templates(self, text: str, variables: dict):
        for key, value in variables.items():
            text = text.replace(f"{{{{{key}}}}}", str(value))
        return text

    async def get_template(self, slug: str, session: AsyncSession):
        result = await session.execute(
            select(Templates).filter(Templates.slug == slug)
        )
        return result.scalars().one_or_none()
        
    async def send_email_notification(self, data, session: AsyncSession):
        slug = data['slug']
        to_email = data['to_email']
        variables = data.get("variables", {})

        template = await self.get_template(slug, session)
        if not template:
            raise Exception("Email template not found")

        subject = self.render_templates(template.subject, variables)
        body = self.render_templates(template.content, variables)

        smtp_service.send_mail(to_email, subject, body, html=True)
        return True

        
common_service = CommonServices()