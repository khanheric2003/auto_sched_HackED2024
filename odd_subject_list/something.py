import re

string = "•  PSYCH 600 - Individual Studies •  PSYCH 622 - Topics in Developmental Psychology •  PSYCH 631 - Topics in Quantitative Methods PSYCH 574 - Advanced Topics in Neuroscience •  PSYCH 496 - Individual Research •  PSYCH 498 - Individual Study II •  PSYCH 491 - Topics in Evolutionary Theory in Psychology •  PSYCH 473 - Advanced Topics in Neuroscience •  PSYCH 458 - Advanced Topics in Cognition •  PSYCH 447 - Self and Identity •  PSYCH 452 - Minds and Machines •  PSYCH 455 - Speech Perception •  PSYCH 443 - Social Cognition •  PSYCH 440 - Advanced Topics in Culture and Psychology •  PSYCH 421 - Advanced Topics in Human Development •  PSYCH 423 - Advanced Topics in Developmental Psychology •  PSYCH 400 - Honors Seminar II •  PSYCH 403 - Recent Advances in Experimental Psychology: Models and Theories •  PSYCH 405 - Special Topics in Psychology II •  PSYCH 409 - Honors Seminar II •  PSYCH 396 - Individual Research •  PSYCH 398 - Individual Study I •  PSYCH 367 - Perception •  PSYCH 350 - Human Memory •  PSYCH 351 - Spatial Cognition •  PSYCH 341 - Cultural Psychology •  PSYCH 342 - Social Influence •  PSYCH 333 - Personality Theory •  PSYCH 305 - Special Topics in Psychology I •  PSYCH 309 - Honors Seminar I •  PSYCH 300 - Honors Seminar I •  PSYCH 302 - Special Topics in Psychological Research •  PSYCH 275 - Brain and Behavior •  PSYCH 241 - Social Psychology"
course_numbers = re.findall(r'\b\d+\b', string)

with open('PSYCH.txt', 'w') as file:
    for number in course_numbers:
        file.write(number + '\n')
