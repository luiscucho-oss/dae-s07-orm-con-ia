import json

from django.core.management.base import BaseCommand, CommandError

from blog.agent.llm import ask_model
from blog.agent.registry import execute


class Command(BaseCommand):
    help = (
        "Pasa una intención por la pasarela de acciones. La intención viene de "
        "--intent (la escribes tú) o de --ask (la propone un modelo local)."
    )

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--intent", help='JSON, p. ej. \'{"action": "posts_per_author", "args": {}}\'')
        group.add_argument("--ask", help="pregunta en lenguaje natural para el modelo local")
        parser.add_argument("--approve", help="hash del plan que un humano aprueba (solo R2)")

    def handle(self, *args, **options):
        if options["ask"] is not None:
            # The model proposes; it never receives --approve.
            try:
                intent = ask_model(options["ask"])
            except (RuntimeError, ValueError, OSError) as exc:
                raise CommandError(f"No se pudo consultar al modelo: {exc}") from exc
            approval = None
            self.stdout.write(f"El modelo propone: {json.dumps(intent, ensure_ascii=False)}")
        else:
            try:
                intent = json.loads(options["intent"])
            except json.JSONDecodeError as exc:
                raise CommandError(f"--intent no es JSON válido: {exc}") from exc
            approval = options["approve"]

        result = execute(intent, approval)
        self.stdout.write(json.dumps(result, ensure_ascii=False, indent=2))
        if result["status"] == "approval_required":
            self.stdout.write(
                self.style.WARNING(
                    "\nNo se aplicó nada. Si TÚ apruebas este plan, repite el comando con "
                    f"--approve {result['plan']['plan_hash']}"
                )
            )
