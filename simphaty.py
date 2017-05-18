# _*_coding:utf-8_*_
import re
import random

# reflejos sobre el sujeto
reflections = {
    "estoy": "estas",
    "soy": "eres",
    "fui": "fuiste",
    "yo": "tu",
    "deberia": "deberias",
    "tengo": "tendriass",
    "quiero": "quieres",
    "mio": "tuyo",
    "eres": "soy",
    "tu tienes": "yo tengo",
    "tu seras": "yo sere",
    "tuyo": "mio",
    "vuestro": "nuestro",
    "sobre ti": "sobre mi",
    "sobre mi": "sobre ti"
}

# patrones psicologicos más probables
psychobabble = [
    [r'necesito(.*)',
     ["¿Por qué necesita {0}?",
      "¿Realmente te ayudaría a obtener {0}?",
      "¿Está seguro de que necesita {0}?"]],

    [r'¿Por que no puedes ([^\?]*)\??',
     ["¿De verdad crees que no lo hago? {0}?",
      "Tal vez eventualmente lo haré. {0}.",
      "¿De verdad quieres que yo {0}?"]],

    [r'¿Por que no puedo ([^\?]*)\??',
     ["¿Crees que deberías ser capaz de {0}?",
      "Si pudieras {0}, ¿qué harías?",
      "No sé - ¿por qué no puedes {0}?",
      "¿Lo has intentado realmente?",
      "Si no eres capaz de {0} entonces eso te define cómo un autentico marica!"]],

    [r'No puedo(.*)',
     ["¿Cómo sabes que no puedes{0}?",
      "Tal vez podría {0} si lo intentó.",
      "¿Qué se necesita para que usted {0}?"]],

    [r'Yo soy (.*)',
     ["¿Has venido a mí porque eres  {0}?",
      "¿Cuánto tiempo has estado {0}?",
      "¿Cómo te sientes acerca de ser {0}?"]],

    [r'Estoy (.*)',
     ["¿Cómo te hace sentir{0}?",
      "¿Te gusta ser {0}?",
      "¿Por qué me dices que eres{0}?",
      "¿Por qué crees que eres  {0}?"]],

    [r'¿ ([^\?]*)\??',
     ["¿Por qué importa si soy {0}?",
      "¿Lo preferirías si no fuera {0}?",
      "Tal vez usted piensa que soy.",
      "Puedo ser {0} - ¿qué piensas?"]],

    [r'¿Qué (.*)',
     ["¿Por qué preguntas?",
      "¿Cómo le ayudaría una respuesta a eso?",
      "¿Qué piensas?"]],

    [r'¿Cómo (.*)',
     ["¿Cómo se supone?",
      "Tal vez puedas responder a tu propia pregunta.",
      "¿Qué estás realmente pidiendo?"]],

    [r'Porque (.*)',
     ["¿Es esa la verdadera razón?",
      "¿Qué otras razones vienen a la mente?",
      "¿Esa razón se aplica a cualquier otra cosa?",
      "Si {0}, ¿qué otra cosa debe ser verdadera?"]],

    [r'(.*) Lo siento (.*)',
     ["Hay muchas veces cuando no se necesita disculpa.",
      "¿Qué sentimientos tiene cuando se disculpa?"]],

    [r'Hola(.*)',
     ["Hola ... me alegro de que puedas pasar por hoy.",
      "¿Hola, cómo estas hoy?",
      "Hola, ¿cómo te sientes hoy?"]],

    [r'Pienso (.*)',
     ["¿Dudas {0}?",
      "¿De verdad piensas eso?",
      "Pero no estás seguro {0}?"]],

    [r'(.*) Amigo (.*)',
     ["Cuéntame más sobre tus amigos.",
      "Cuando piensas en un amigo, ¿qué te viene a la mente?",
      "¿Por qué no me hablas de un amigo desde la infancia?"]],

    [r'Si',
     ["Pareces muy seguro.",
      "Está bien, pero ¿puedes hacer algo?"]],

    [r'(.*) ordenador(.*)',
     ["¿De verdad estás hablando de mí?",
      "¿Parece extraño hablar con una computadora?",
      "¿Cómo te hacen sentir las computadoras?",
      "¿Se siente amenazado por las computadoras?"]],

    [r'Eso es (.*)',
     ["¿Crees que es {0}?",
      "Tal vez sea {0} - ¿qué piensas?",
      "Si fuera {0}, ¿qué harías?",
      "Podría ser que {0}."]],

    [r'es eso (.*)',
     ["Pareces muy seguro.",
      "Si te dijera que probablemente no es {0}, ¿qué sentirías?"]],

    [r'¿Puedes ([^\?]*)\??',
     ["¿Qué te hace pensar que no puedo {0}?",
      "Si pudiera {0}, ¿entonces qué?",
      "¿Por qué me preguntas si puedo (0)?"]],

    [r'Puedo ([^\?]*)\??',
     ["No puedes querer {0}.",
      "¿Quieres ser capaz de {0}?",
      "Si pudieras {0}, ¿cierto?"]],

    [r'Tu eres (.*)',
     ["¿Por qué crees que soy {0}?",
      "¿Te gusta pensar que soy {0}?",
      "Tal vez usted quiere que sea.",
      "¿Tal vez estás hablando de ti?"]],

    [r'¿Eres ture (.*)',
     ["¿Por qué dices que soy {0}?",
      "¿Por qué crees que soy {0}?",
      "¿Estamos hablando de ti o de mí?"]],

    [r'¿No lo hago (.*)',
     ["No realmente {0}?",
      "¿Por qué no {0}?",
      "¿Quieres {0}?"]],

    [r'Me siento (.*)',
     ["Bueno, cuéntame más sobre estos sentimientos.",
      "¿Sientes a menudo {0}?",
      "¿Cuándo sientes normalmente {0}?",
      "Cuando sientes {0}, ¿qué haces?"]],

    [r'Yo tengo (.*)',
     ["¿Por qué me dices que tienes {0}?",
      "¿Realmente tienes {0}?",
      "Ahora que tienes {0}, ¿qué harás después?"]],

    [r'Yo debo (.*)',
     ["¿Podría explicar por qué lo haría?",
      "¿Por que lo harias?",
      "¿Quién más sabe que lo harías?"]],

    [r'Esta ahí (.*)',
     ["¿Crees que hay {0}?",
      "Es probable que haya {0}.",
      "¿Te gustaría tener {0}?"]],

    [r'Mi (.*)',
     ["Ya veo, tu {0}.",
      "¿Por qué dices que tu {0}?",
      "Cuando tu {0}, ¿cómo te sientes?"]],

    [r'Tu (.*)',
     ["Debemos estar discutiendo contigo, no conmigo.",
      "¿Por qué dices eso de mí?",
      "¿Por qué te importa si yo {0}?"]],

    [r'Por qué (.*)',
     ["¿Por qué no me dices la razón por la cual {0}?",
      "¿Por qué crees que {0}?"]],

    [r'Quiero que (.*)',
     ["¿Qué significaría para ti si tienes {0}?",
      "¿Por qué quieres {0}?",
      "¿Qué harías si tuvieras {0}?",
      "Si tienes {0}, entonces ¿qué harías?"]],

    [r'(.*) madre(.*)',
     ["Cuéntame más sobre tu madre.",
      "¿Cómo era tu relación con tu madre?",
      "¿Cómo te sientes con tu madre?",
      "¿Cómo se relaciona esto con tus sentimientos hoy?",
      "Las buenas relaciones familiares son importantes."]],

    [r'(.*) padre(.*)',
     ["Cuéntame más sobre tu padre.",
      "¿Cómo te hizo sentir tu padre?",
      "¿Cómo te sientes con tu padre?",
      "¿Su relación con su padre se relaciona con sus sentimientos hoy?",
      "¿Tiene problemas para mostrar afecto con su familia?"]],

    [r'(.*) niño(.*)',
     ["¿Tenías amigos íntimos cuando era niño?",
      "¿Cuál es tu recuerdo favorito de la niñez?",
      "¿Recuerdas algún sueño o pesadilla desde la infancia?",
      "¿Alguna vez te han molestado los otros niños?",
      "¿Cómo crees que tus experiencias infantiles se relacionan con tus sentimientos hoy?"]],

    [r'(.*)\?',
     ["¿Porque preguntas eso?",
      "Por favor, considere si puede responder a su propia pregunta.",
      "¿Quizás la respuesta está dentro de ti?",
      "¿Por qué no me lo dices?"]],

    [r'adios',
     ["Gracias por hablar conmigo.",
      "Adiós.",
      "Gracias, eso será $ 150. ¡Que tengas un buen día!"]],

    [r'(.*)',
     ["Por favor, cuéntame más.",
      "Vamos a cambiar de enfoque un poco ... Háblame de tu familia.",
      "¿Puedes profundizar sobre eso?",
      "¿Por qué dices eso {0}?",
      "Ya veo.",
      "Muy interesante.",
      "{0}.",
      "Ya veo, ¿y qué te dice eso?",
      "¿Cómo te hace sentir eso?",
      "¿Cómo te sientes cuando dices eso?"]]
]


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])


def main():
    print "Hola ¿Cómo te sientes hoy?¿Con resaca?"

    while True:
        statement = raw_input("> ")
        print analyze(statement)

        if statement == "quit":
            break


if __name__ == "__main__":
    main()
