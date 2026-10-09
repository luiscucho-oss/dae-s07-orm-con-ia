from django.core.management.base import BaseCommand, CommandError

from blog.duel.questions import BY_KEY
from blog.duel.runner import SOURCES, STATUS_LABEL, run_all


class Command(BaseCommand):
    help = "Corre las ocho preguntas del duelo contra tus respuestas (o las de la IA)."

    def add_arguments(self, parser):
        parser.add_argument("--source", choices=sorted(SOURCES), default="team",
                            help="de quién son las respuestas (por defecto: team = las tuyas)")
        parser.add_argument("--question", choices=sorted(BY_KEY),
                            help="correr solo una pregunta, p. ej. q4")
        parser.add_argument("--strict", action="store_true",
                            help="terminar con error si alguna no es correcta")

    def handle(self, *args, **options):
        try:
            verdicts = run_all(options["source"], options["question"])
        except ModuleNotFoundError as exc:
            raise CommandError(f"No hay respuestas de «{options['source']}»: {exc}") from exc

        self.stdout.write(f"\nDuelo — respuestas de: {options['source']}\n")
        for verdict in verdicts:
            question = BY_KEY[verdict.key]
            queries = f"{verdict.queries} consulta(s)" if verdict.status != "todo" else ""
            self.stdout.write(
                f"{verdict.key}  {STATUS_LABEL[verdict.status]:<24} {queries:<16}"
                f"{question.text[:60]}"
            )
            if verdict.detail:
                self.stdout.write(f"      └─ {verdict.detail}")

        good = sum(1 for verdict in verdicts if verdict.status == "ok")
        self.stdout.write(f"\n{good} de {len(verdicts)} correctas y baratas.\n")
        if options["strict"] and good != len(verdicts):
            raise CommandError("Hay respuestas que no son correctas.")
