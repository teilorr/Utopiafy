from __future__ import annotations

from random import Random
import re

random = Random()

data = """
#template:
@member@ é @mood@ @adjetive@
Eu acho que @member@ é @mood@ @adjetive@
Não é por nada não, mas @member@ é @mood@ @adjetive@
Não consigo saber de tudo, mas sei que @member@ é @mood@ @adjetive@
Cá entre nós, @member@ é @mood@ @adjetive@
#end

#adjetive:
gay
viado
homem
macho
chad
sigma
alpha
femêa
mulherzinha
bluepill
redpill
homem de verdade
utopier
randola
mod
gordo
pobre
viadinho
guilhermevilarpando
#end

#mood:
muito
100%
extremamente
com certeza
com toda certeza
sem dúvidas
definitivamente
obviamente
#end
"""


# Heeeyyy! Ideia de gerador por Sebastian Lague!
class IdeiaGenerator:
    def get_category(self, category_name) -> str:
        start_tag = f"#{category_name}:\n"
        end_tag = "\n#end"
        return self.get_text_between_tags(data, start_tag, end_tag).split("\n")

    def get_text_between_tags(self, text: str, start_tag: str, end_tag: str):
        return text.split(start_tag)[1].split(end_tag)[0]

    def pick_random(self, category_name: str):
        return random.choice(self.get_category(category_name))

    def generate_mood(self):
        return self.pick_random("mood")

    def generate_adjetive(self):
        return self.pick_random("adjetive")

    def fill_template(self, template: str, member: str) -> str:
        template = template.replace("@member@", member)
        matches: list[str] = re.findall(r"\@(.*?\@)", template)
        
        for generator in matches:
            generator = generator.removesuffix("@")
            match generator:
                case "mood":
                    replacement = self.generate_mood()

                case "adjetive":
                    replacement = self.generate_adjetive()

            template = template.replace(generator, replacement).replace("@", "")
        return template

    def generate(self, member: str):
        return self.fill_template(self.pick_random("template"), member=member)
