define a node n
n <- T is good if it has infintely many descendants
Root r is good

path := [r, ..., nk]
nk is good by IH (induction hypothesis):

nk has finitely many children at least one is good, pick one, let it be nk+1
Continue forever

sound only proves valid things
complete proves arbitrary valid things

you must use a fair schedule

semi-decidable logic