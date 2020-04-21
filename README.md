# OneStopQA

OneStopQA is a multiple choice reading comprehension dataset annotated according to the STARC (Structured Annotations for Reading Comprehension) scheme. The reading materials are Guardian articles taken from the [OneStopEnglish corpus](https://github.com/nishkalavallabhi/OneStopEnglishCorpus). Each article comes in three difficlty levels, Elementary, Intermediate and Advanced. Each paragraph is annotated with three multiple choice reading comprehension questions. The reading comprehension questions can be answered based on any of the three paragraph levels.

# STARC Annotation Structure

| Answer | Description | Textual Span | Annotation Tag
| --- | --- | --- | --- |
| a | Correct answer. | Critical Span | A |
| b | Incorrect answer. A miscomprehension of the critical span. | Critical Span |A|
| c | Incorrect answer. Refers to an additional span. | Distractor Span | D|
| d | Incorrect answer. Has no textual support. | - | - |

# Example

Leading water scientists have issued one of the sternest warnings yet about global food supplies, saying that the world’s population may have to switch almost completely to a vegetarian diet by 2050 to avoid catastrophic shortages. \<D\>Humans derive about 20% of their protein from animal-based products now, but this may need to drop to just 5% to feed the extra two billion people expected to be alive by 2050,\</D\> according to research by some of the world’s leading water scientists. \<A\>“There will not be enough water available on current croplands to produce food for the expected nine-billion population in 2050 if we follow current trends and changes towards diets common in western nations,” the report by Malik Falkenmark and colleagues at the Stockholm International Water Institute (SIWI) said.\</A\>

Q: According to Malik Falkenmark’s report, what will happen if the world adopts the current diet trends of western nations?  
a: There will not be sufficient water to grow enough food for everyone  
b: By 2050, nine billion people will not have enough drinking water  
c: By 2050, animal-based protein consumption will reduce from 20% to 5%  
d: Obesity rates around the world will rise  

# Statistics
Aricles: 30  
Paragraphs: 162  
Questions: 486  
Question-Paragraph Level pairs: 1,458  

# Citation
```
@inproceedings{starc2020,  
      author    = {Berzak, Yevgeni and Malmaud, Jonathan and Levy, Roger},  
      title     = {STARC: Structured Annotations for Reading Comprehension},  
      booktitle = {ACL},  
      year      = {2020},  
      publisher = {Association for Computational Linguistics} 
      }
```

# License
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

