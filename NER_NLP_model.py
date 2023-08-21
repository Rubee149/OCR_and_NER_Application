import spacy
from spacy import displacy

spacy.cli.download("en_core_web_sm")
NER = spacy.load("en_core_web_sm")

def spacy_large_ner(document):
  return {(ent.text.strip(), ent.label_) for ent in NER(document).ents}

doc="The World Health Organization (WHO)[1] is a specialized agency of the United Nations responsible for international public health.[2] The WHO Constitution states its main objective as 'the attainment by all peoples of the highest possible level of health'.[3] Headquartered in Geneva, Switzerland, it has six regional offices and 150 field offices worldwide. The WHO was established on 7 April 1948.[4][5] The first meeting of the World Health Assembly (WHA), the agency's governing body, took place on 24 July of that year. The WHO incorporated the assets, personnel, and duties of the League of Nations' Health Organization and the Office International d'Hygiène Publique, including the International Classification of Diseases (ICD).[6] Its work began in earnest in 1951 after a significant infusion of financial and technical resources.[7]"

#spacy_large_ner(doc)

#spacy.explain("ORG")

displacy.serve(NER(doc),style="ent")