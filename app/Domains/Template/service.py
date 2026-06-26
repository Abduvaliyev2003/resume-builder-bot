from app.Shared.api_client import api


class TemplateService:

    async def get_templates(self):

        return await api.get("/templates")


    async def get_template(
        self,
        template_id: str,
    ):

        return await api.get(
            f"/templates/{template_id}"
        )


template_service = TemplateService()