#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, PlaceType, Place

engine = create_engine('sqlite:///nuevomexico.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create four dummy users
User1 = User(name="Tom Chavez",
        email="tom.chavez@gmail.com",
        picture="http://i32.photobucket.com/albums/d1/beningcampbell/tom_chavez_zpsscj8qwe1.jpg")  # NOQA
session.add(User1)
session.commit()

User2 = User(
    name="Chris Baca",
    email="chris.baca@gmail.com",
    picture="http://i32.photobucket.com/albums/d1/beningcampbell/chris_baca_zpsv1rl8nio.jpg")  # NOQA
session.add(User2)
session.commit()

User3 = User(
    name="Johanna Martinez",
    email="johanna.martinez@gmail.com",
    picture="http://i32.photobucket.com/albums/d1/beningcampbell/johanna_martinez_zpsqztin6h2.jpg")  # NOQA
session.add(User3)
session.commit()

User4 = User(
    name="Sarah Garcia",
    email="sarah.garcia@gmail.com",
    picture="http://i32.photobucket.com/albums/d1/beningcampbell/sarah_garcia_zpsfbpue51l.jpg")  # NOQA
session.add(User4)
session.commit()


# Create a place type called Restaurants
placeType1 = PlaceType(name="Restaurants", user_id=2)
session.add(placeType1)
session.commit()

restaurant1 = Place(
    name="El Pinto",
    description="El Pinto started serving New Mexican food in 1962 and is \
    one of the most popular New Mexican restaurants in Albuquerque. \
    Located on a 12-acre piece of property in Albuquerque's North Valley, \
    El Pinto has five dining patios. Make sure to pick up a jar (or two) \
    of El Pinto salsa on your way out. 10500 4th St. NW, Albuquerque.",
    location="Albuquerque area",
    price="$$",
    link="https://www.elpinto.com",
    placeType=placeType1)
session.add(restaurant1)
session.commit()

restaurant2 = Place(
    name="The Shed",
    description="Located a block away from Santa Fe's Plaza, The Shed \
    serves some of the best New Mexican food in the state. Expect long \
    lines and lots of tourists, but the food is worth it. Their red chile \
    is especially good. Dinner is by reservation only. 113.5 East Palace \
    Avenue, Santa Fe.",
    location="Santa Fe area",
    price="$$",
    link="https://www.sfshed.com",
    placeType=placeType1)
session.add(restaurant2)
session.commit()

restaurant3 = Place(
    name="Orlando's New Mexican Cafe",
    description="Orlando's New Mexican Cafe has won lots of awards (best \
    green chile, best red chile, best New Mexican food in Taos, \
    etc). If you ever find yourself anywhere near Taos, make sure to \
    stop by Orlando's. 1114 Don Juan Valdez Ln, Taos.",
    location="Northern New Mexico",
    price="$$",
    link="https://www.facebook.com/OrlandosNewMexicanCafe/",
    placeType=placeType1)
session.add(restaurant3)
session.commit()

restaurant4 = Place(
    name="Frontier Restaurant",
    description="The Frontier Restaurant is big--it has room for more \
    than 300 people. Located in downtown Albuquerque across the street \
    from the University of New Mexico, Frontier is a popular student \
    spot and is open every day until 1:00 am. Make sure to try one of \
    their legendary breakfast burritos. 2400 Central Ave SE, Albuquerque.",
    location="Albuquerque area",
    price="$",
    link="http://www.frontierrestaurant.com/",
    placeType=placeType1)
session.add(restaurant4)
session.commit()

restaurant5 = Place(
    name="Tomasita's Restaurant",
    description="Tomasita's has been around for more than 40 years and \
    serves classic Northern New Mexican food. Try their blue corn \
    enchiladas. 500 S Guadalupe St, Santa Fe.",
    location="Santa Fe area",
    price="$$",
    link="http://tomasitas.com/",
    placeType=placeType1)
session.add(restaurant5)
session.commit()


# Create a place type called Pueblos
placeType2 = PlaceType(name="Pueblos", user_id=4)
session.add(placeType2)
session.commit()

pueblo1 = Place(
    name="Acoma",
    description="Known as Sky City, Acoma Pueblo is located on top of \
    a sandstone mesa measuring 365 feet high. Once only accessible by a \
    very steep and narrow path up the side of the mesa, the pueblo can \
    now by reached by road. Acoma Pueblo is located 50 miles to the west \
    of Albuquerque. Admission is $23 for adults, $15 for children and \
    $20 for seniors. Guided walking tours are available. While audio and \
    video recordings are not allowed, photography is permitted (for a fee).",
    location="Albuquerque area",
    price="$$",
    link="http://www.acomaskycity.org/home.html",
    placeType=placeType2)
session.add(pueblo1)
session.commit()

pueblo2 = Place(
    name="Taos",
    description="Taos Pueblo is about 1.5 hours north of Santa Fe and is \
    known for its multi-story apartment dwellings. Admission is $10 per \
    adult and $5 for students. Expect a fee of $5 per camera and $5 per \
    video camera (please note that cameras are not permitted on feast days).",
    location="Northern New Mexico",
    price="$",
    link="http://taospueblo.com",
    placeType=placeType2)
session.add(pueblo2)
session.commit()

pueblo3 = Place(
    name="Tesuque",
    description="Only about 10 miles to the north of Santa Fe, Tesuque \
    Pueblo is believed to have been settled before 1200 AD. Artists at \
    Tesque are known for their pottery and model figurines. The pueblo \
    does not charge for admission; however, photography is not allowed.",
    location="Santa Fe area",
    price="Free",
    link="https://www.newmexico.org/tesuque-pueblo/",
    placeType=placeType2)
session.add(pueblo3)
session.commit()

pueblo4 = Place(
    name="Indian Pueblo Cultural Center",
    description="Located in Albuquerque, the Indian Pueblo Cultural Center \
    is a great place to start learning about New Mexico's pueblos and \
    their history, culture and art. Admission is $8.50 for adults, $6.40 \
    for seniors (and New Mexico residents) and $5.40 for children. (There \
    is no charge for children under 5.) 2401 12th ST NW, Albuquerque.",
    location="Albuquerque area",
    price="$",
    link="http://www.indianpueblo.org/",
    placeType=placeType2)
session.add(pueblo4)
session.commit()

pueblo5 = Place(
    name="San Felipe",
    description="San Felipe Pueblo is located about 30 miles to the \
    northwest of Albuquerque. The pueblo is usually not open to visitors. \
    However, visitors are welcome to visit the pueblo during the Annual \
    Feast Day (May 1).",
    location="Albuquerque area",
    price="Free",
    link="https://www.newmexico.org/san-felipe-pueblo/",
    placeType=placeType2)
session.add(pueblo5)
session.commit()


# Create a place type called Parks and monuments
placeType3 = PlaceType(name="Parks and monuments", user_id=1)
session.add(placeType3)
session.commit()

parkAndMon1 = Place(
    name="White Sands National Monument",
    description="White Sands National Monument is a 275-square-mile \
    expanse of white sand dunes made up of gypsum crystals. Located \
    approximately 15 miles to the southwest of Alamogordo, White Sands \
    is the largest area of gypsum crystal dunes in the world. It can get \
    quite hot in southern New Mexico in the summer, so a visit to White \
    Sands would be best in the spring or fall. And make sure to bring \
    sunglasses; white sand on a sunny day is very bright!",
    location="Southern New Mexico",
    price="$",
    link="https://www.nps.gov/whsa/index.htm",
    placeType=placeType3)
session.add(parkAndMon1)
session.commit()

parkAndMon2 = Place(
    name="Bandelier National Monument",
    description="Bandelier National Monument is a group of pueblo structures \
    and nearby land. The structures were probably built sometime between 1150 \
    and 1600 AD. The monument is located about 40 miles northwest of Santa Fe \
    and covers 50 square miles of a plateau in the Jemez Mountains. Many of \
    the dwellings are carved into the side of rock cliffs, and visitors can \
    enter some of them. The site is spectacular. Visitors will get the most \
    out of their visit if they read up on the history of the site before \
    visiting it.",
    location="Santa Fe area",
    price="$$",
    link="https://www.nps.gov/band/index.htm",
    placeType=placeType3)
session.add(parkAndMon2)
session.commit()

parkAndMon3 = Place(
    name="Carlsbad Caverns National Park",
    description="Located just 10 miles north of the U.S.-Mexico border, \
    Carlsbad Caverns is a cave system in the Guadalupe Mountains. Some of \
    the underground caverns have a ceiling height of as much as 250 feet. \
    The caves are generally fairly cool (around 56 degrees F \
    (13 degrees C), so make sure to bring warm clothes. Visitors may \
    take self-guided or guided tours.",
    location="Southern New Mexico",
    price="$",
    link="https://www.nps.gov/cave/index.htm",
    placeType=placeType3)
session.add(parkAndMon3)
session.commit()

parkAndMon4 = Place(
    name="Gila Cliff Dwellings National Monument",
    description="Located around 30 miles to the north of Silver City, \
    the remote Gila Cliff Dwellings were built by the Mogollon peoples \
    more than 700 years ago. The monument is surrounded by the Gila \
    National Forest and covers about 550 acres of land. Viewing the \
    dwellings can be done by hiking a short one-mile trail.",
    location="Southern New Mexico",
    price="$",
    link="https://www.nps.gov/gicl/index.htm",
    placeType=placeType3)
session.add(parkAndMon4)
session.commit()

parkAndMon5 = Place(
    name="Chaco Culture National Historical Park",
    description="Chaco Culture National Historical Park is located about \
    50 miles southeast of Farmington and around 100 miles northwest of \
    Albuquerque. The monument reportedly contains the most dense collection \
    of pueblos in the southwest. The area was a cultural hub sometime \
    between 850 and 1250 AD. Visitors can use hiking and biking trails, \
    and guided tours are available.",
    location="Northern New Mexico",
    price="$",
    link="https://www.nps.gov/chcu/index.htm",
    placeType=placeType3)
session.add(parkAndMon5)
session.commit()


# Create a place type called Museums
placeType4 = PlaceType(name="Museums", user_id=2)
session.add(placeType4)
session.commit()

museum1 = Place(
    name="New Mexico Museum of Art",
    description="Established almost 100 years ago (under the name of \
    the Art Gallery for the Museum of New Mexico), the New Mexico \
    Museum of Art is located just off the Santa Fe Plaza. The museum has a \
    great collection of southwestern art and several Georgia O'Keeffe pieces. \
    General admission is $12 per person, $7 for New Mexico residents, and \
    there is no fee for those under 16. 107 West Palace Avenue, Santa Fe.",
    location="Santa Fe area",
    price="$",
    link="http://nmartmuseum.org/",
    placeType=placeType4)
session.add(museum1)
session.commit()

museum2 = Place(
    name="Georgia O'Keeffe Museum",
    description="Just four blocks northwest of the Santa Fe Plaza, the \
    Georgia O'Keefe Museum opened in 1997 and houses more than 3,000 pieces \
    by O'Keeffe as well as information about how she approached her work. \
    Georgia O'Keeffe spent a large part of her life living and working in \
    New Mexico. Admission is $12; New Mexico students can enter for $8. 217 \
    Johnson Street, Santa Fe.",
    location="Santa Fe area",
    price="$",
    link="https://www.okeeffemuseum.org/",
    placeType=placeType4)
session.add(museum2)
session.commit()

museum3 = Place(
    name="Museum of Indian Arts and Culture",
    description="Along with several other museums, the Museum of Indian \
    Arts and Culture is located about three miles away from downtown Santa \
    Fe on Museum Hill in the Sangre de Cristo Mountains. The museum is a \
    great place to start learning about southwest Native American culture \
    and tradition. Visit the nearby Wheelwright Museum of the American \
    Indian, the Museum of Spanish Colonial Art and the Museum of \
    International Folk Art while you're in the neighborhood. Admission is \
    $12 for non-New Mexican residents, and $7 for residents. 710 Camino Lejo \
    off Old Santa Fe Trail, Santa Fe.",
    location="Santa Fe area",
    price="$",
    link="http://www.indianartsandculture.org/",
    placeType=placeType4)
session.add(museum3)
session.commit()

museum4 = Place(
    name="Museum of Natural History and Science",
    description="Albuquerque's Museum of Natural History and Science was \
    established in 1986 and is located only a few blocks away from the Old \
    Town Plaza. The museum has a number of permanent exhibits that \
    highlight the early years of the Earth's history; the dinosaur exhibits \
    are perhaps the museum's best. Admission is $7 for adults and $4 for \
    children (age 12 years and under). 1801 Mountain Road NW, Albuquerque.",
    location="Albuquerque area",
    price="$",
    link="http://www.nmnaturalhistory.org/",
    placeType=placeType4)
session.add(museum4)
session.commit()

museum5 = Place(
    name="New Mexico Museum of Space History",
    description="The New Mexico Museum of Space History is located in \
    the southern New Mexico town of Alamogordo, which is about a \
    three-hour's drive from Albuquerque. A Smithsonian Affiliate, the \
    museum includes a planetarium and is home to the International Space \
    Hall of Fame. Some of the museum's artifacts are very large; for \
    example, the Little Joe II rocket, which was used to test the Apollo \
    Launch Escape System, measures 86 feet in height. Admission is $7 for \
    adults and $4 for children (age 12 years and under). 3198 State Route \
    2001, Alamogordo.",
    location="Southern New Mexico",
    price="$",
    link="http://www.nmspacemuseum.org/",
    placeType=placeType4)
session.add(museum5)
session.commit()


# Create a place type called Shopping spots
placeType5 = PlaceType(name="Shopping spots", user_id=3)
session.add(placeType5)
session.commit()

shoppingSpot1 = Place(
    name="Jackalope",
    description="While it is not the best place for purchasing authentic \
    New Mexican merchandise (Jackalope imports many of it's products \
    from Mexico), it is still a great place to purchase Southwest-style \
    home decor. Open everyday, 9am-6pm. 2820 Cerrillos Rd., Santa Fe.",
    location="Santa Fe area",
    price="$ - $$$",
    link="http://jackalope.com/",
    placeType=placeType5)
session.add(shoppingSpot1)
session.commit()

shoppingSpot2 = Place(
    name="Shiprock Santa Fe",
    description="Shiprock Santa Fe is a gallery and store run by a \
    fifth-generation Indian art dealer by the name of Jed Foutz. Browse \
    through an impressive collection of Navajo rugs and textiles, jewelry, \
    furniture, pottery and more. Shiprock Santa Fe is located on the Santa \
    Fe Plaza. Open Monday through Friday, 10am-5pm, Saturday, 12pm-5pm, and \
    by appointment. 53 Old Santa Fe Trail, Santa Fe.",
    location="Santa Fe area",
    price="$$ - $$$$",
    link="http://www.shiprocksantafe.com/beta/",
    placeType=placeType5)
session.add(shoppingSpot2)
session.commit()

shoppingSpot3 = Place(
    name="Albuquerque Old Town",
    description="Comprising roughly ten blocks, Albuquerque Old Town has \
    played a significant role in in the city since Albuquerque was founded \
    over 300 years ago. Enjoy roaming through Old Town's streets, gardens \
    and brick paths while exploring the many shops and galleries \
    (more than 150) in the area. 303 Romero St N.W., Albuquerque.",
    location="Albuquerque area",
    price="$ - $$$$",
    link="http://www.albuquerqueoldtown.com/",
    placeType=placeType5)
session.add(shoppingSpot3)
session.commit()

shoppingSpot4 = Place(
    name="Santa Fe Plaza",
    description="The Santa Fe Plaza--or simply, the Plaza--has remained the \
    center of downtown Santa Fe for close to 400 years. Surrounded by \
    shops and restaurants, the Plaza is a good place to explore a wide \
    variety of New Mexican handicrafts. Make sure to spend some time \
    browsing through the handmade jewelry, pottery and art sold by street \
    vendors under a long portal on the northeastern side of the Plaza \
    (the portal fronts the Palace of the Governors, a history museum and \
    the oldest public building in the country). The street vendors are part \
    of a tradition spanning 80 years and are selected on a lottery basis, \
    meaning that a particular vendor may be at the Plaza one day and not \
    the next. Feel free to ask how pieces were made and what material was \
    used. 105 W Palace Avenue, Santa Fe.",
    location="Santa Fe area",
    price="$ - $$$$",
    link="http://santafe.org/perl/page.cgi?p=maps;gid=2401",
    placeType=placeType5)
session.add(shoppingSpot4)
session.commit()

shoppingSpot5 = Place(
    name="El Rincon Trading Post",
    description="Started by a German trader named Ralph Meyers, El Rincon \
    Trading Post turned 100 in 2009. When Meyers opened the shop, New Mexico \
    was not a state, but Taos was a well-known center for trading everything \
    from livestock to pottery. El Rincon Trading Post is a great place to \
    browse through Native American crafts and jewelry. You can also find Old \
    West souvenirs. Open 10am-5pm. 114 Kit Carson Rd., Taos.",
    location="Northern New Mexico",
    price="$ - $$$",
    link="http://www.lonelyplanet.com/usa/southwest/taos/shopping/fashion-accessories/el-rincon-trading-post",  # NOQA
    placeType=placeType5)
session.add(shoppingSpot5)
session.commit()


# Create a place type called Outdoor activities
placeType6 = PlaceType(name="Outdoor activities", user_id=4)
session.add(placeType6)
session.commit()

outdoor1 = Place(
    name="Albuquerque International Balloon Fiesta",
    description="Every October Albuquerque hosts the largest balloon \
    fiesta in the world. More than 500 hot-air balloons typically \
    participate in the nine-day event. A number of special events \
    are held each year including pre-dawn flights, special shape \
    flights and a mass launch when large groups of balloons take off \
    at the same time.",
    location="Albuquerque area",
    price="$",
    link="http://balloonfiesta.com/",
    placeType=placeType6)
session.add(outdoor1)
session.commit()

outdoor2 = Place(
    name="Taos Ski Valley",
    description="Located about 35 miles north of Taos, the legendary \
    Taos Ski Valley is in the Sangre de Cristo mountains. Its \
    relatively new Kachina lift takes skiers up to an elevation of \
    close to 12,500 feet (3,800 meters). Taos was long known to be a \
    skier-only resort, but snowboarders were welcomed to the mountain \
    in 2008. Summer activities at Taos Ski valley include hiking and \
    biking trails, scenic lift rides and disc golf.",
    location="Northern New Mexico",
    price="$$$",
    link="https://www.skitaos.com/",
    placeType=placeType6)
session.add(outdoor2)
session.commit()

outdoor3 = Place(
    name="Angel Fire Ski Resort",
    description="Angel Fire is well known for its ski runs (it has 80). \
    And it offers two terrain parks and over 30 acres of tree skiing. \
    However, Angel Fire also has a lot of options for those visiting \
    in the summer, including a golf course, hiking and biking trails \
    and zipline tours.",
    location="Northern New Mexico",
    price="$$$",
    link="http://www.angelfireresort.com/",
    placeType=placeType6)
session.add(outdoor3)
session.commit()

outdoor4 = Place(
    name="Paa-Ko Ridge Golf Club",
    description="Located to the east of the Sandia mountains, the \
    27-hole Paa-Ko Rdige Golf Club has received a lot of national \
    attention, including being ranked as the 58th best public golf \
    facility in the nation, according to Golf Digest. The club is \
    located about twenty minutes away from Albuquerque.",
    location="Albuquerque area",
    price="$$$",
    link="http://www.paakoridge.com/",
    placeType=placeType6)
session.add(outdoor4)
session.commit()

outdoor5 = Place(
    name="La Luz Trail",
    description="The La Luz trail is a great way to see the \
    Albuquerque valley from several thousand feet up. The trail \
    starts in the foothills on the northeast side of Albuquerque \
    and ascends 8.7 miles (14 km) up the west side of the Sandia \
    Mountains. The altitude range is over 3,000 feet (900 meters), \
    and the trail is rated as difficult. Hikers can get a bite to \
    eat at the High Finance restaurant at the top of the mountain and \
    take the Sandia Tram back down.",
    location="Albuquerque area",
    price="Free",
    link="http://www.laluztrail.com/",
    placeType=placeType6)
session.add(outdoor5)
session.commit()


print "Added new places"
