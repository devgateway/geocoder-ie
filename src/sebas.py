from matplotlib import pylab
from nltk.tokenize.texttiling import TextTilingTokenizer

tt = TextTilingTokenizer()
text = """1. INTRODUCTION
The proposed projects’ main activity during the implementation Phase is the completion of construction of workshops, 
laboratories, classrooms, offices, and other support structures for Butere Technical Training Institute (TTI) located in Butere District, Kakamega County; Aldai TTI located in Nandi South district, Nandi County; Bureti TTI located in Bureti district, Kericho County; Godoma TTI located in Ganze District, Kilifi County; Mukurweini TTI located in Mukuruwe-ini District, Nyeri County; Siala TTI located at Rongo sub County, Migori County; Tseikuru TTI located in Tseikuru district, Kitui County; and Wajir TTI located in 
Wajir East District, Wajir County. After completion of this phase the Institutions’ 
main activity shall be training of the youth, which involves use of training equipment in the workshops and the laboratories.
2. BRIEF PROJECT DESCRIPTION AND KEY COMPONENTS
Component I: Improve Access, Quality and Relevance of TVET: The project proposes to support completion of engineering and applied sciences workshops/ laboratories in the eight TTIs1 under Phase 1; complete procurement of the remaining sets of engineering and applied sciences equipment from some of the Phase 12 target TTIs. Furthermore, this sub-component will also support provision of equipment and training at the upcoming Mpeketoni TTI in Lamu. The vocational in Turkana, Lowdar Youth Polytechnic is currently being upgraded by the County Government and the private sector, mainly Tullow Oil, as a Centre of Excellence in Oil related trainings. 
These TTIs are located in areas where key projects such as the LAPPSET, 
railway, oil and wind projects are situated."""
s, ss, d, b = tt.tokenize(text)
