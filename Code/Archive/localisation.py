import requests, sys

requestURL = "https://www.ebi.ac.uk/proteins/api/coordinates?offset=0&size=100&gene=YFL066C"

r = requests.get(requestURL, headers={ "Accept" : "text/x-gff"})

if not r.ok:
  r.raise_for_status()
  sys.exit()

responseBody = r.text
print(responseBody)

##gff-version 3
##sequence-region P43538 1 392
#P43538	UniProtKB	domain	1	175	.	-	.	Note=Helicase ATP-binding.;GenomeLocStart=2615;GenomeLocEnd=2091;Chromosome=VI;EnsemblTranslationId=YFL066C;EnsemblGeneId=YFL066C;EnsemblTranscriptId=YFL066C_mRNA
#P43538	UniProtKB	nucleotide phosphate-binding region	11	18	.	-	.	Note=ATP.;GenomeLocStart=2585;GenomeLocEnd=2562;Chromosome=VI;EnsemblTranslationId=YFL066C;EnsemblGeneId=YFL066C;EnsemblTranscriptId=YFL066C_mRNA
#P43538	UniProtKB	domain	232	381	.	-	.	Note=Helicase C-terminal.;GenomeLocStart=1922;GenomeLocEnd=1473;Chromosome=VI;EnsemblTranslationId=YFL066C;EnsemblGeneId=YFL066C;EnsemblTranscriptId=YFL066C_mRNA



for line in responseBody.split('\n'):
	for word in line.split(';'):
		if word.startswith('Genome'):
			print(word)
