from rapidfuzz import fuzz
from typing import Dict, Any

TARGET_TEXT = (
	"Oportunidade | Desenvolvedor(a) Frontend Jr, (Início imediato).\n"
	"Estamos buscando um(a) Desenvolvedor Frontend para atuar 100% home office\n"
	"Se você quer trabalhar com React.js, Redux e GraphQL em um ambiente dinâmico e inovador, essa vaga pode ser para você.\n"
	"Regime: PJ\n"
	"Modelo: Home-Office\n"
	"Salário a combinar.\n"
	"Requisitos\n"
	"Conhecimento em React.js (hooks, ciclo de vida)\n"
	"1 ano de experiência com Material-UI (ou outra biblioteca de componentes)\n"
	"Diferenciais:\n"
	"Projetos focados em engajamento e usabilidade\n"
	"Conhecimento em Git, CI/CD e metodologias ágeis\n"
	"Noções de Redux e GraphQL\n"
	"Interessados(as): envie currículo e o link do seu LinkedIn pelo chat.\n"
	"#desenvolvedor #tecnologia #vagas #vagashomeoffice"
)

PRIMARY_KEYWORDS = [
    "Frontend Jr",
    "Desenvolvedor Frontend",
    "React.js",
    "Redux",
    "GraphQL",
    "Material-UI",
    "home office",
    "remoto",
    "remote",
]

SIMILAR_TECH = [
    "React",
    "React.js",
    "Hooks",
    "Material UI",
    "MUI",
    "Component library",
    "Next.js",
    "Redux",
    "GraphQL",
    "Git",
    "CI/CD",
    "Agile",
    "TypeScript",
    "JavaScript",
    "Node.js",
    "Python",
]

REQUIRED_REMOTE_MARKERS = [
    "home office",
    "remoto",
    "remote",
    "100% remote",
    "work from home",
]


def score_exact_match(text: str) -> int:
    return int(fuzz.token_set_ratio(text, TARGET_TEXT))


def score_similar_job(text: str) -> Dict[str, Any]:
    scores: Dict[str, Any] = {}
    scores["base"] = int(fuzz.partial_token_set_ratio(text, " ".join(SIMILAR_TECH)))
    scores["keywords"] = sum(1 for k in PRIMARY_KEYWORDS if k.lower() in text.lower())
    scores["remote"] = any(k in text.lower() for k in [m.lower() for m in REQUIRED_REMOTE_MARKERS])
    scores["overall"] = scores["base"] + scores["keywords"] * 10 + (10 if scores["remote"] else 0)
    return scores


EXACT_THRESHOLD = 92
SIMILAR_THRESHOLD = 55
