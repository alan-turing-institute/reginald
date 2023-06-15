import pathlib
import re

csv_in = pathlib.Path("data/public/turingacuk.csv")
csv_out = pathlib.Path("data/public/turingacuk-no-boilerplate.csv")
with open(csv_in, "r") as f:
    content = f.read()

boilerplates = [
    r"""Section page
Conferences, workshops, and other events from around the Turing University Network
A series of inspiring talks by leading figures in data science and AI
The Turing works with a range of partners with far-reaching, real-world impact across sectors
The Institute's podcast for discussions on all things data science, AI and machine learning
To make great leaps in research, we need to better reflect the diverse nature of the world
Research projects
The Turing and its partners have invested more than £26m in digital twin research and innovation
Publication
Research spotlight
Enrichment student Premdeep Gill is studying Antarctic seals and their sea ice habitats through satellite data, to better understand how they are coping with climate change
Research spotlight
As co-lead of the Turing’s Women in Data Science and AI project, Research Fellow Erin Young’s vital research maps the gendered career trajectories in data science and AI
Applications have now closed
Section page
Events bringing together some of the country’s top talent from data science, artificial intelligence, and wider fields, to analyse real-world data science challenges
We work with a wide range of partners to help deliver our mission of changing the world using data science and artificial intelligence
Sign up to our monthly newsletter, receive our exclusive Turing events guide, get updates from our applied skills programme and keep in touch with new research opportunities
Find out more about the expert commentary the Turing can provide""",
    r"""© The Alan Turing Institute
2023. All rights reserved.
The Alan Turing Institute, a charity incorporated and registered in England and Wales with company number 09512457 and charity number 1162533 whose registered office is at British Library, 96 Euston Road, London, England, NW1 2DB, United Kingdom.
For website-related enquiries email
[email protected]

Explore the Institute
Section page
Conferences, workshops, and other events from around the Turing University Network
A series of inspiring talks by leading figures in data science and AI
The Turing works with a range of partners with far-reaching, real-world impact across sectors
The Institute's podcast for discussions on all things data science, AI and machine learning
To make great leaps in research, we need to better reflect the diverse nature of the world
Research projects
The Turing and its partners have invested more than £26m in digital twin research and innovation
Publication
Research spotlight
Enrichment student Premdeep Gill is studying Antarctic seals and their sea ice habitats through satellite data, to better understand how they are coping with climate change
Research spotlight
As co-lead of the Turing’s Women in Data Science and AI project, Research Fellow Erin Young’s vital research maps the gendered career trajectories in data science and AI
Applications have now closed
Section page
Events bringing together some of the country’s top talent from data science, artificial intelligence, and wider fields, to analyse real-world data science challenges
We work with a wide range of partners to help deliver our mission of changing the world using data science and artificial intelligence
Sign up to our monthly newsletter, receive our exclusive Turing events guide, get updates from our applied skills programme and keep in touch with new research opportunities
Find out more about the expert commentary the Turing can provide
Legal
Awards
""",
    r"""© The Alan Turing Institute
2023. All rights reserved.
The Alan Turing Institute, a charity incorporated and registered in England and Wales with company number 09512457 and charity number 1162533 whose registered office is at British Library, 96 Euston Road, London, England, NW1 2DB, United Kingdom.
For website-related enquiries email
[email protected]

Explore the Institute

Legal
Awards
""",
    r"""© The Alan Turing Institute
 2023. All rights reserved.
The Alan Turing Institute, a charity incorporated and registered in England and Wales with company number 09512457 and charity number 1162533 whose registered office is at British Library, 96 Euston Road, London, England, NW1 2DB, United Kingdom.
For website-related enquiries email
[email protected]

Explore the Institute

Legal
Awards
""",
    r"""© The Alan Turing Institute
2023. All rights reserved.
The Alan Turing Institute, a charity incorporated and registered in England and Wales with company number 09512457 and charity number 1162533 whose registered office is at British Library, 96 Euston Road, London, England, NW1 2DB, United Kingdom.
For website-related enquiries email
we[email protected]

Explore the Institute

Legal
Awards
""",
    r"""© The Alan Turing Institute 2023. All rights reserved.
The Alan Turing Institute, a charity incorporated and registered in England and Wales with company number 09512457 and charity number 1162533 whose registered office is at British Library, 96 Euston Road, London, England, NW1 2DB, United Kingdom.
For website-related enquiries email [email protected]
""",
]

for b in boilerplates:
    content = content.replace(b, "")

with open(csv_out, "w") as f:
    f.write(content)
