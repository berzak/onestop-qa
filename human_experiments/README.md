# Human reading comprehension experiments with OneStopQA and [RACE](https://www.aclweb.org/anthology/D17-1082.pdf).

`prolific/`  
Experiments ran on [Prolific](https://www.prolific.co/).
Each experiment has 1296 items (648 OneStopQA, and 648 RACE test set), with three participants per item, 972 participants, and 6 items per participant (2 practice items + 4 experiment items).

- `prolific/qa.tsv` Participants are presented with a passage along with a question and its four answers, and are asked to select the correct answer based on the passage.

- `prolific/guess.tsv` Participants see only the question and its four answers and are asked to provide their best guess for the correct answer.

- `prolific/judge.tsv` Participants are presented with the question, answers and the passage, and are asked to indicate whether the question has (A) one correct answer, (B) more than one correct answer, or (C) no correct answer. If (A) is selected, the participant further selects the correct answer. If (B) is selected, the participant is asked to mark all the answers that they consider to be correct.

`in_lab/qa_mit_lab.tsv`  
QA Experiment ran with MIT students in lab. The task is identical to the prolific question answering experiment.  
432 items (216 OneStopQA, and 216 RACE test set), with one participant per item, 12 participants, 36 items per participant. 

# Notes

`item_id`:  
OneStopQA: os[article \#]\_[paragraph \#]\_[question \#]\_[difficulty level]  
RACE: r[file name]\_[question \#]\_[difficulty level]

OnesStopQA items are taken from the following 20 articles:

|\#	| file name |
| --- | --- |
|1	| Google-introduces-its-driverless-car.txt	|
|2	| Love-hormone-helps-autistic-children-bond-with-others.txt	|
|3	| Spain's-robin-hood.txt |
|4  |	Will-drones-soon-be-delivering-packages-to-your-doorstep.txt	|
|5	| Philip-pullman-illegal-downloading-is-moral-squalor.txt	|
|6  |	Swarthy-blue-eyed-caveman-revealed.txt |
|7	| Inky-the-octopus-escapes-from-aquarium.txt	|
|8  |	Autumn-born-children-better-at-sport-says-study.txt	|
|9  |	Why-you-should-start-work-at-10am.txt	|
|10 | The-Greek-island-where-time-is-running-out.txt |
|11 | The-secrets-of-the-mystery-shopper.txt	|
|12 |On-the-trail-of-the-wolf.txt |
|13 |Why-is-Sweden-closing-its-prisons.txt	|
|14 |Four-new-elements-find-a-place-on-periodic-table.txt|
|15 |	A-new-form-of-lie-detector-test.txt	|
|16 |	Vienna-named-worlds-top-city-for-quality-of-life.txt|
|17 |	Wealth-therapy-for-the-rich.txt	|
|18 |	Rwandan-women-whip-up-popular-ice-cream-business.txt |
|19 |	Bolivians-demand-the-right-to-chew-coca-leaves.txt	|
|20 |	Insects-could-be-the-planets-next-food-source.txt	|

**Known Issues**

- `prolfic/qa.tsv` and `prolific/guess.tsv` miss 2 participants (so that 8 experiment items have only 2 responses).
- `in_lab/qa_mit_lab.tsv` misses 2 items. 
