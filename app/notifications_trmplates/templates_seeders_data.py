from app.models.signup_models import Templates
from app.notifications_trmplates.signup_templates_json import signup_templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


class TemplatesSeeders:
    @staticmethod
    async def run_seeders(session: AsyncSession):
        """
        Check if notification templates exist by slug.
        Update existing ones or insert new ones.
        """
        for template in signup_templates:
            slug = template["notification_slug"]

            result = await session.execute(select(Templates).where(Templates.slug == slug))
            existing_template = result.scalar_one_or_none()

            if existing_template:

                existing_template.template_name = template["notification_name"]
                existing_template.subject = template["subject"]
                existing_template.content = template["content"]
                existing_template.variables = template["variables"]
                existing_template.notification_type = template["notification_type"]
                print(f"Updated template: {slug}")
            else:

                new_template = Templates(
                    id=str(uuid.uuid4()),
                    slug=slug,
                    template_name=template["notification_name"],
                    subject=template["subject"],
                    content=template["content"],
                    variables=template["variables"],
                    notification_type=template["notification_type"],
                )
                session.add(new_template)
                print(f"Created template: {slug}")

        await session.commit()
        print("Notification template seeding complete.")
