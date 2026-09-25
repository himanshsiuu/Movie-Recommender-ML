"""
Himanshu's Movie & Series Directory - Production Two-Tower Recommendation Engine
Encodes User and Movie/Series items into dense embedding vectors for vector cosine similarity retrieval.
Includes full IMDb ratings, synopsis briefs, cast credits, awards, and direct IMDb links.
"""

import math
import random
from typing import List, Dict, Any

# Expanded Master Movie & Series Catalog across All Genres (121 Acclaimed Titles)
MOVIES_CATALOG = [
    {
        "id": "m_01",
        "title": "Blade Runner 2049",
        "year": 2017,
        "genres": [
            "Sci-Fi",
            "Mystery",
            "Drama"
        ],
        "director": "Denis Villeneuve",
        "rating": 8.0,
        "match_keywords": [
            "neon",
            "dystopia",
            "replicant",
            "cyberpunk"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf06 Flying spinner through glowing orange dust storm",
            "emotional": "\ud83c\udf27\ufe0f K sitting on snowy steps listening to rain"
        },
        "imdb_id": "tt1856101",
        "imdb_url": "https://www.imdb.com/title/tt1856101/",
        "plot": "Thirty years after the events of Blade Runner (1982), a new Blade Runner, L.A.P.D. Officer \"K\" (Ryan Gosling), unearths a long-buried secret that has the potential to plunge what's left of society into chaos. K's discovery leads him on a quest to find Rick Deckard (Harrison Ford), a former L.A.P.D. Blade Runner, who has been missing for thirty years.",
        "actors": "Harrison Ford, Ryan Gosling, Ana de Armas",
        "runtime": "164 min",
        "rated": "R",
        "awards": "Won 2 Oscars. 100 wins & 164 nominations total",
        "metascore": "81",
        "imdb_votes": "751,317",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "gCcx85zbxz4",
        "clip_url": "https://www.youtube-nocookie.com/embed/gCcx85zbxz4",
        "clip_title": "Official Teaser \u2014 2049 Replicant Revelation",
        "clip_duration": "2:31",
        "sound_theme": "Sci-Fi Vangelis Synth & Sub-Bass"
    },
    {
        "id": "m_02",
        "title": "Interstellar",
        "year": 2014,
        "genres": [
            "Sci-Fi",
            "Adventure",
            "Drama"
        ],
        "director": "Christopher Nolan",
        "rating": 8.7,
        "match_keywords": [
            "space",
            "black hole",
            "relativity",
            "wormhole"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\ude80 Endurance spaceship spinning through Gargantua wormhole",
            "emotional": "\u23f3 Cooper weeping watching 23 years of family video logs"
        },
        "imdb_id": "tt0816692",
        "imdb_url": "https://www.imdb.com/title/tt0816692/",
        "plot": "In the near future around the American Midwest, Cooper, an ex-science engineer and pilot, is tied to his farming land with his daughter Murph and son Tom. As devastating sandstorms ravage Earth's crops, the people of Earth realize their life here is coming to an end as food begins to run out. Eventually stumbling upon a N.A.S.A. base 6 hours from Cooper's home, he is asked to go on a daring mission with a few other scientists into a wormhole because of Cooper's scientific intellect and ability to pilot aircraft unlike the other crew members. In order to find a new home while Earth decays, Cooper must decide to either stay, or risk never seeing his children again in order to save the human race by finding another habitable planet.",
        "actors": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "runtime": "169 min",
        "rated": "PG-13",
        "awards": "Won 1 Oscar. 45 wins & 148 nominations total",
        "metascore": "74",
        "imdb_votes": "2,516,752",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "zSWdZVtXT7E",
        "clip_url": "https://www.youtube-nocookie.com/embed/zSWdZVtXT7E",
        "clip_title": "Official Trailer \u2014 Gargantua & Hans Zimmer Pipe Organ",
        "clip_duration": "2:44",
        "sound_theme": "Epic Hans Zimmer Pipe Organ & Space Vacuum"
    },
    {
        "id": "m_03",
        "title": "The Matrix",
        "year": 1999,
        "genres": [
            "Sci-Fi",
            "Action"
        ],
        "director": "Lana & Lilly Wachowski",
        "rating": 8.7,
        "match_keywords": [
            "matrix",
            "cyberpunk",
            "simulation",
            "neo"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udd76\ufe0f Neo bullet-time rooftop dodge in slow motion",
            "emotional": "\ud83d\udc8a Morpheus offering red pill vs blue pill"
        },
        "imdb_id": "tt0133093",
        "imdb_url": "https://www.imdb.com/title/tt0133093/",
        "plot": "Thomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination. Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government. As a rebel against the machines, Neo must confront the agents: super-powerful computer programs devoted to stopping Neo and the entire human rebellion.",
        "actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "runtime": "136 min",
        "rated": "R",
        "awards": "Won 4 Oscars. 42 wins & 52 nominations total",
        "metascore": "73",
        "imdb_votes": "2,243,093",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "vKQi3bBA1y8",
        "clip_url": "https://www.youtube-nocookie.com/embed/vKQi3bBA1y8",
        "clip_title": "Official Trailer \u2014 The Red Pill & Cyberpunk Beats",
        "clip_duration": "2:27",
        "sound_theme": "Cyberpunk Industrial Breakbeats & Synth Hits"
    },
    {
        "id": "m_04",
        "title": "Inception",
        "year": 2010,
        "genres": [
            "Sci-Fi",
            "Action",
            "Adventure"
        ],
        "director": "Christopher Nolan",
        "rating": 8.8,
        "match_keywords": [
            "dreams",
            "heist",
            "subconscious",
            "totem"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfd9\ufe0f Paris city street folding overhead in zero gravity",
            "emotional": "\ud83c\udf00 Spinning pewter totem on the table"
        },
        "imdb_id": "tt1375666",
        "imdb_url": "https://www.imdb.com/title/tt1375666/",
        "plot": "Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction, stealing valuable secrets from deep within the subconscious during the dream state, when the mind is at its most vulnerable. Cobb's rare ability has made him a coveted player in this treacherous new world of corporate espionage, but it has also made him an international fugitive and cost him everything he has ever loved. Now Cobb is being offered a chance at redemption. One last job could give him his life back but only if he can accomplish the impossible, inception. Instead of the perfect heist, Cobb and his team of specialists have to pull off the reverse: their task is not to steal an idea, but to plant one. If they succeed, it could be the perfect crime. But no amount of careful planning or expertise can prepare the team for the dangerous enemy that seems to predict their every move. An enemy that only Cobb could have seen coming.",
        "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "runtime": "148 min",
        "rated": "PG-13",
        "awards": "Won 4 Oscars. 160 wins & 220 nominations total",
        "metascore": "74",
        "imdb_votes": "2,811,614",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "YoHD9XEInc0",
        "clip_url": "https://www.youtube-nocookie.com/embed/YoHD9XEInc0",
        "clip_title": "Official Trailer \u2014 Non, Je Ne Regrette Rien Horns",
        "clip_duration": "2:30",
        "sound_theme": "Mind-Bending Inception Brass Horns & Ticking"
    },
    {
        "id": "m_05",
        "title": "Dune: Part Two",
        "year": 2024,
        "genres": [
            "Sci-Fi",
            "Adventure",
            "Action"
        ],
        "director": "Denis Villeneuve",
        "rating": 8.6,
        "match_keywords": [
            "desert",
            "spice",
            "sandworm",
            "prophecy"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTc0YmQxMjEtODI5MC00NjFiLTlkMWUtOGQ5NjFmYWUyZGJhXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfdc\ufe0f Paul Atreides mounting the colossal Shai-Hulud sandworm",
            "emotional": "\ud83c\udf05 Sunset duel on the Arrakis golden dunes"
        },
        "imdb_id": "tt15239678",
        "imdb_url": "https://www.imdb.com/title/tt15239678/",
        "plot": "Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family. Facing a choice between the love of his life and the fate of the known universe, he endeavors to prevent a terrible future only he can foresee.",
        "actors": "Timoth\u00e9e Chalamet, Zendaya, Rebecca Ferguson",
        "runtime": "166 min",
        "rated": "PG-13",
        "awards": "Won 2 Oscars. 125 wins & 376 nominations total",
        "metascore": "79",
        "imdb_votes": "734,902",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "Way9Dexny3w",
        "clip_url": "https://www.youtube-nocookie.com/embed/Way9Dexny3w",
        "clip_title": "Official Trailer 3 \u2014 Paul Atreides & Desert War Cry",
        "clip_duration": "2:56",
        "sound_theme": "Arrakis War Chants & Hans Zimmer Ethnic Percussion"
    },
    {
        "id": "m_26",
        "title": "The Prestige",
        "year": 2006,
        "genres": [
            "Sci-Fi",
            "Drama",
            "Mystery"
        ],
        "director": "Christopher Nolan",
        "rating": 8.5,
        "match_keywords": [
            "magic",
            "rivalry",
            "tesla",
            "illusion"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTM3MzQ5MjQ5OF5BMl5BanBnXkFtZTcwMTQ3NzMzMw@@._V1_QL75_UY562_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u26a1 Tesla electrical lightning machine in snow field",
            "emotional": "\ud83c\udfa9 Dual magicians bowing on Victorian stage"
        },
        "imdb_id": "tt0482571",
        "imdb_url": "https://www.imdb.com/title/tt0482571/",
        "plot": "Set in London in the 1800s, two rival magicians read each others diary containing the secrets of their magic tricks and personal life. As we go back in time when the diaries were written, both magicians become obsessed with their rival's best trick. The tricks, as shown to the audience, look the same, but neither magician can figure out how his opponent does it.",
        "actors": "Christian Bale, Hugh Jackman, Scarlett Johansson",
        "runtime": "130 min",
        "rated": "PG-13",
        "awards": "Nominated for 2 Oscars. 6 wins & 44 nominations total",
        "metascore": "66",
        "imdb_votes": "1,583,310",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "o4gHCmTQDVI",
        "clip_url": "https://www.youtube-nocookie.com/embed/o4gHCmTQDVI",
        "clip_title": "Official Trailer \u2014 The Prestige & Transported Man",
        "clip_duration": "2:25",
        "sound_theme": "Victorian Mystery Orchestra & Clockwork Cello"
    },
    {
        "id": "m_27",
        "title": "Arrival",
        "year": 2016,
        "genres": [
            "Sci-Fi",
            "Drama",
            "Mystery"
        ],
        "director": "Denis Villeneuve",
        "rating": 7.9,
        "match_keywords": [
            "linguistics",
            "aliens",
            "time",
            "heptapod"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udef8 Giant alien shell hovering in Montana mist",
            "emotional": "\ud83d\udd8b\ufe0f Drawing circular logogram on transparent glass"
        },
        "imdb_id": "tt2543164",
        "imdb_url": "https://www.imdb.com/title/tt2543164/",
        "plot": "Linguistics professor Louise Banks leads an elite team of investigators when gigantic spaceships touchdown in 12 locations around the world. As nations teeter on the verge of global war, Banks and her crew must race against time to find a way to communicate with the extraterrestrial visitors. Hoping to unravel the mystery, she takes a chance that could threaten her life and quite possibly all of mankind.",
        "actors": "Amy Adams, Jeremy Renner, Forest Whitaker",
        "runtime": "116 min",
        "rated": "PG-13",
        "awards": "Won 1 Oscar. 71 wins & 268 nominations total",
        "metascore": "81",
        "imdb_votes": "852,057",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "tFMo3UJ4B4g",
        "clip_url": "https://www.youtube-nocookie.com/embed/tFMo3UJ4B4g",
        "clip_title": "Official Trailer \u2014 Heptapod Language & Max Richter Strings",
        "clip_duration": "2:24",
        "sound_theme": "Lush Ambient Vocal Resonance & Sub-Drone"
    },
    {
        "id": "m_28",
        "title": "The Martian",
        "year": 2015,
        "genres": [
            "Sci-Fi",
            "Adventure",
            "Drama"
        ],
        "director": "Ridley Scott",
        "rating": 8.0,
        "match_keywords": [
            "mars",
            "botany",
            "nasa",
            "survival"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTc2MTQ3MDA1Nl5BMl5BanBnXkFtZTgwODA3OTI4NjE@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\ude80 Launching rover through martian red dust storm",
            "emotional": "\ud83c\udf31 First green potato sprout inside Mars habitat"
        },
        "imdb_id": "tt3659388",
        "imdb_url": "https://www.imdb.com/title/tt3659388/",
        "plot": "During a manned mission to Mars, Astronaut Mark Watney is presumed dead after a fierce storm and left behind by his crew. But Watney has survived and finds himself stranded and alone on the hostile planet. With only meager supplies, he must draw upon his ingenuity, wit and spirit to subsist and find a way to signal to Earth that he is alive. Millions of miles away, NASA and a team of international scientists work tirelessly to bring \"the Martian\" home, while his crewmates concurrently plot a daring, if not impossible, rescue mission. As these stories of incredible bravery unfold, the world comes together to root for Watney's safe return.",
        "actors": "Matt Damon, Jessica Chastain, Kristen Wiig",
        "runtime": "144 min",
        "rated": "PG-13",
        "awards": "Nominated for 7 Oscars. 40 wins & 199 nominations total",
        "metascore": "80",
        "imdb_votes": "999,128",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "ej3ioOneTy8",
        "clip_url": "https://www.youtube-nocookie.com/embed/ej3ioOneTy8",
        "clip_title": "Official Trailer \u2014 Bring Him Home & Disco Grooves",
        "clip_duration": "2:47",
        "sound_theme": "Uplifting Space Disco & Planetary Acoustic Chords"
    },
    {
        "id": "m_29",
        "title": "Ex Machina",
        "year": 2014,
        "genres": [
            "Sci-Fi",
            "Drama",
            "Thriller"
        ],
        "director": "Alex Garland",
        "rating": 7.7,
        "match_keywords": [
            "ai",
            "turing test",
            "robot",
            "consciousness"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTUxNzc0OTIxMV5BMl5BanBnXkFtZTgwNDI3NzU2NDE@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83e\udd16 Ava revealing robotic glass skin & neural core",
            "emotional": "\ud83e\ude9e Caleb staring into one-way mirror in secluded facility"
        },
        "imdb_id": "tt0470752",
        "imdb_url": "https://www.imdb.com/title/tt0470752/",
        "plot": "Caleb, a 26 year old programmer at the world's largest internet company, wins a competition to spend a week at a private mountain retreat belonging to Nathan, the reclusive CEO of the company. But when Caleb arrives at the remote location he finds that he will have to participate in a strange and fascinating experiment in which he must interact with the world's first true artificial intelligence, housed in the body of a beautiful robot girl.",
        "actors": "Alicia Vikander, Domhnall Gleeson, Oscar Isaac",
        "runtime": "108 min",
        "rated": "R",
        "awards": "Won 1 Oscar. 74 wins & 162 nominations total",
        "metascore": "78",
        "imdb_votes": "633,967",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "EoQuVnKhxaM",
        "clip_url": "https://www.youtube-nocookie.com/embed/EoQuVnKhxaM",
        "clip_title": "Official Trailer \u2014 Ava Turing Test & Synth Pulse",
        "clip_duration": "2:32",
        "sound_theme": "Minimalist Digital Glockenspiel & Low Resonance"
    },
    {
        "id": "m_30",
        "title": "Tenet",
        "year": 2020,
        "genres": [
            "Sci-Fi",
            "Action",
            "Thriller"
        ],
        "director": "Christopher Nolan",
        "rating": 7.3,
        "match_keywords": [
            "inversion",
            "entropy",
            "time",
            "espionage"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTIzNDIxMzktMzlkMi00MmUyLWFmMjQtZDgwMjBmOGJmNTI3XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\ude97 Backward highway car crash reverse explosion",
            "emotional": "\u23f3 Inverted bullet flying back into operator hand"
        },
        "imdb_id": "tt6723592",
        "imdb_url": "https://www.imdb.com/title/tt6723592/",
        "plot": "In a twilight world of international espionage, an unnamed CIA operative, known as The Protagonist, is recruited by a mysterious organization called Tenet to participate in a global assignment that unfolds beyond real time. The mission: prevent Andrei Sator, a renegade Russian oligarch with precognitive abilities, from starting World War III. The Protagonist will soon master the art of \"time inversion\" as a way of countering the threat that is to come.",
        "actors": "John David Washington, Robert Pattinson, Elizabeth Debicki",
        "runtime": "150 min",
        "rated": "PG-13",
        "awards": "Won 1 Oscar. 49 wins & 135 nominations total",
        "metascore": "69",
        "imdb_votes": "709,795",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "LdOM0x0XDMo",
        "clip_url": "https://www.youtube-nocookie.com/embed/LdOM0x0XDMo",
        "clip_title": "TENET - Official Trailer",
        "clip_duration": "3:05",
        "sound_theme": "Reverse Audio Riser & Heavy Sub-Bass Pulses"
    },
    {
        "id": "m_31",
        "title": "Edge of Tomorrow",
        "year": 2014,
        "genres": [
            "Sci-Fi",
            "Action",
            "Adventure"
        ],
        "director": "Doug Liman",
        "rating": 7.9,
        "match_keywords": [
            "time loop",
            "mimics",
            "exo suit",
            "beach"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTc5OTk4MTM3M15BMl5BanBnXkFtZTgwODcxNjg3MDE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2694\ufe0f Full-metal jacket exo-suit battle on Normandy beach",
            "emotional": "\u23f1\ufe0f Live Die Repeat reset awakening at base"
        },
        "imdb_id": "tt1631867",
        "imdb_url": "https://www.imdb.com/title/tt1631867/",
        "plot": "An alien race has hit the Earth in an unrelenting assault, unbeatable by any military unit in the world. Major William Cage (Cruise) is an officer who has never seen a day of combat when he is unceremoniously dropped into what amounts to a suicide mission. Killed within minutes, Cage now finds himself inexplicably thrown into a time loop-forcing him to live out the same brutal combat over and over, fighting and dying again...and again. But with each battle, Cage becomes able to engage the adversaries with increasing skill, alongside Special Forces warrior Rita Vrataski (Blunt). And, as Cage and Vrataski take the fight to the aliens, each repeated encounter gets them one step closer to defeating the enemy!",
        "actors": "Tom Cruise, Emily Blunt, Bill Paxton",
        "runtime": "113 min",
        "rated": "PG-13",
        "awards": "11 wins & 38 nominations total",
        "metascore": "71",
        "imdb_votes": "802,767",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "vw61gCe2oqI",
        "clip_url": "https://www.youtube-nocookie.com/embed/vw61gCe2oqI",
        "clip_title": "Official Trailer \u2014 Live. Die. Repeat. Mimic Roar",
        "clip_duration": "2:29",
        "sound_theme": "Fast Adrenaline Synth Arpeggio & Combat FX"
    },
    {
        "id": "m_32",
        "title": "Avatar: The Way of Water",
        "year": 2022,
        "genres": [
            "Sci-Fi",
            "Action",
            "Adventure"
        ],
        "director": "James Cameron",
        "rating": 7.6,
        "match_keywords": [
            "pandora",
            "ocean",
            "navi",
            "tulkun"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNWI0Y2NkOWEtMmM2OC00MjQ3LWI1YzItZGQxYzQ3NzI4NWZmXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udf0a Skimming ocean waves on winged Ilu creature",
            "emotional": "\ud83c\udf0c Sully family breathing under bioluminescent reef"
        },
        "imdb_id": "tt1630029",
        "imdb_url": "https://www.imdb.com/title/tt1630029/",
        "plot": "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race to protect their home.",
        "actors": "Sam Worthington, Zoe Salda\u00f1a, Sigourney Weaver",
        "runtime": "192 min",
        "rated": "PG-13",
        "awards": "Won 1 Oscar. 74 wins & 153 nominations total",
        "metascore": "67",
        "imdb_votes": "601,100",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "d9MyW72ELq0",
        "clip_url": "https://www.youtube-nocookie.com/embed/d9MyW72ELq0",
        "clip_title": "Official Trailer \u2014 Pandora Ocean Depth & Choral Swell",
        "clip_duration": "2:28",
        "sound_theme": "Bioluminescent Choral Swells & Tribal Drums"
    },
    {
        "id": "m_33",
        "title": "Her",
        "year": 2013,
        "genres": [
            "Sci-Fi",
            "Drama",
            "Romance"
        ],
        "director": "Spike Jonze",
        "rating": 8.0,
        "match_keywords": [
            "ai",
            "love",
            "future",
            "os"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA1Nzk0OTM2OF5BMl5BanBnXkFtZTgwNjU2NjEwMDE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf06 Theodore running through vibrant neon future Los Angeles",
            "emotional": "\ud83c\udfa7 Listening to Samantha voice at golden hour sunset"
        },
        "imdb_id": "tt1798709",
        "imdb_url": "https://www.imdb.com/title/tt1798709/",
        "plot": "Theodore is a lonely man in the final stages of his divorce. When he's not working as a letter writer, his down time is spent playing video games and occasionally hanging out with friends. He decides to purchase the new OS1, which is advertised as the world's first artificially intelligent operating system, \"It's not just an operating system, it's a consciousness,\" the ad states. Theodore quickly finds himself drawn in with Samantha, the voice behind his OS1. As they start spending time together they grow closer and closer and eventually find themselves in love. Having fallen in love with his OS, Theodore finds himself dealing with feelings of both great joy and doubt. As an OS, Samantha has powerful intelligence that she uses to help Theodore in ways others hadn't, but how does she help him deal with his inner conflict of being in love with an OS?",
        "actors": "Joaquin Phoenix, Amy Adams, Scarlett Johansson",
        "runtime": "126 min",
        "rated": "R",
        "awards": "Won 1 Oscar. 83 wins & 187 nominations total",
        "metascore": "91",
        "imdb_votes": "725,639",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "dJTU48_yghs",
        "clip_url": "https://www.youtube-nocookie.com/embed/dJTU48_yghs",
        "clip_title": "Her Official Trailer #1",
        "clip_duration": "2:31",
        "sound_theme": "Gentle Neo-Vintage Piano & Warm Ambient Tape"
    },
    {
        "id": "m_66",
        "title": "2001: A Space Odyssey",
        "year": 1968,
        "genres": [
            "Sci-Fi",
            "Adventure"
        ],
        "director": "Stanley Kubrick",
        "rating": 8.3,
        "match_keywords": [
            "hal 9000",
            "monolith",
            "space",
            "stargate"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNjU0NDFkMTQtZWY5OS00MmZhLTg3Y2QtZmJhMzMzMWYyYjc2XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udf0c Stargate psychedelic light tunnel warp",
            "emotional": "\ud83d\udd34 HAL 9000 glowing red eye in quiet cockpit"
        },
        "imdb_id": "tt0062622",
        "imdb_url": "https://www.imdb.com/title/tt0062622/",
        "plot": "\"2001\" is a story of evolution. Sometime in the distant past, someone or something nudged evolution by placing a monolith on Earth (presumably elsewhere throughout the universe as well). Evolution then enabled humankind to reach the moon's surface, where yet another monolith is found, one that signals the monolith placers that humankind has evolved that far. Now a race begins between computers (HAL) and human (Bowman) to reach the monolith placers. The winner will achieve the next step in evolution, whatever that may be.",
        "actors": "Keir Dullea, Gary Lockwood, William Sylvester",
        "runtime": "149 min",
        "rated": "G",
        "awards": "Won 1 Oscar. 18 wins & 14 nominations total",
        "metascore": "84",
        "imdb_votes": "772,787",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "oR_e9y-bka0",
        "clip_url": "https://www.youtube-nocookie.com/embed/oR_e9y-bka0",
        "clip_title": "Official 4K Trailer \u2014 Also Sprach Zarathustra & Monolith",
        "clip_duration": "2:15",
        "sound_theme": "Richard Strauss Epic Tympani & Monolith Choirs"
    },
    {
        "id": "m_67",
        "title": "The Truman Show",
        "year": 1998,
        "genres": [
            "Comedy",
            "Drama",
            "Sci-Fi"
        ],
        "director": "Peter Weir",
        "rating": 8.2,
        "match_keywords": [
            "reality tv",
            "escape",
            "dome",
            "jim carrey"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzA3ZjZlNzYtMTdjMy00NjMzLTk5ZGYtMTkyYzNiOGM1YmM3XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\u26f5 Truman sailing sailboat into edge of sky dome",
            "emotional": "\ud83d\udeaa Bowing and saying: In case I don't see ya, good afternoon, good evening and good night!"
        },
        "imdb_id": "tt0120382",
        "imdb_url": "https://www.imdb.com/title/tt0120382/",
        "plot": "Since birth, a big fat lie defines the well-organised but humdrum life of the kind-hearted insurance salesman and ambitious explorer, Truman Burbank. Utterly unaware of the thousands of cleverly hidden cameras watching his every move, for nearly three decades, Truman's entire existence pivots around the will and the wild imagination of the ruthlessly manipulative television producer, Christof--the all-powerful TV-God of an extreme 24/7 reality show: The Truman Show. As a result, Truman's picturesque neighbourhood with the manicured lawns and the uncannily perfect residents is nothing but an elaborate state-of-the-art set, and the only truth he knows is what the worldwide television network and its deep financial interests dictate. Do lab rats know they are forever imprisoned?",
        "actors": "Jim Carrey, Ed Harris, Laura Linney",
        "runtime": "103 min",
        "rated": "PG",
        "awards": "Nominated for 3 Oscars. 42 wins & 69 nominations total",
        "metascore": "90",
        "imdb_votes": "1,356,843",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "dlnmQbPGuls",
        "clip_url": "https://www.youtube-nocookie.com/embed/dlnmQbPGuls",
        "clip_title": "Official Trailer \u2014 Seahaven Island & Philip Glass Piano",
        "clip_duration": "2:24",
        "sound_theme": "Charming Minimalist Glass Piano & Nostalgic Chords"
    },
    {
        "id": "m_06",
        "title": "The Dark Knight",
        "year": 2008,
        "genres": [
            "Action",
            "Crime",
            "Drama"
        ],
        "director": "Christopher Nolan",
        "rating": 9.0,
        "match_keywords": [
            "joker",
            "batman",
            "gotham",
            "vigilante"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udccf Batmobile semi-truck flip in central Gotham avenue",
            "emotional": "\ud83d\udd25 Joker hanging out police car window into night wind"
        },
        "imdb_id": "tt0468569",
        "imdb_url": "https://www.imdb.com/title/tt0468569/",
        "plot": "Set within a year after the events of Batman Begins (2005), Batman, Lieutenant James Gordon, and new District Attorney Harvey Dent successfully begin to round up the criminals that plague Gotham City, until a mysterious and sadistic criminal mastermind known only as \"The Joker\" appears in Gotham, creating a new wave of chaos. Batman's struggle against The Joker becomes deeply personal, forcing him to \"confront everything he believes\" and improve his technology to stop him. A love triangle develops between Bruce Wayne, Dent, and Rachel Dawes.",
        "actors": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "runtime": "152 min",
        "rated": "PG-13",
        "awards": "Won 2 Oscars. 163 wins & 165 nominations total",
        "metascore": "85",
        "imdb_votes": "3,161,907",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "EXeTwQWrcwY",
        "clip_url": "https://www.youtube-nocookie.com/embed/EXeTwQWrcwY",
        "clip_title": "Official Trailer \u2014 Why So Serious? Joker Theme",
        "clip_duration": "2:30",
        "sound_theme": "Rising Single-Note Joker Cello & Percussive Hits"
    },
    {
        "id": "m_34",
        "title": "John Wick: Chapter 4",
        "year": 2023,
        "genres": [
            "Action",
            "Crime",
            "Thriller"
        ],
        "director": "Chad Stahelski",
        "rating": 7.7,
        "match_keywords": [
            "high table",
            "gun fu",
            "paris",
            "assassin"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BY2Q2ZmI5ZjUtNWVhMC00YzJkLTlmYjMtY2RmZDhkNzEzYjZhXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udd25 Dragon breath shotgun fight in Paris top-down mansion",
            "emotional": "\u26ea Lighting candle at Sacre-Coeur steps before sunrise duel"
        },
        "imdb_id": "tt10366206",
        "imdb_url": "https://www.imdb.com/title/tt10366206/",
        "plot": "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes.",
        "actors": "Keanu Reeves, Laurence Fishburne, George Georgiou",
        "runtime": "169 min",
        "rated": "R",
        "awards": "38 wins & 51 nominations total",
        "metascore": "78",
        "imdb_votes": "405,485",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "qEVUtrk8_B4",
        "clip_url": "https://www.youtube-nocookie.com/embed/qEVUtrk8_B4",
        "clip_title": "Official Trailer \u2014 Continental Duel & Techno Mayhem",
        "clip_duration": "2:30",
        "sound_theme": "Heavy Darkwave Electro Synth & Gunfire Rhythms"
    },
    {
        "id": "m_35",
        "title": "Top Gun: Maverick",
        "year": 2022,
        "genres": [
            "Action",
            "Drama"
        ],
        "director": "Joseph Kosinski",
        "rating": 8.2,
        "match_keywords": [
            "f-18",
            "mach 10",
            "pilot",
            "dogfight"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDBkZDNjMWEtOTdmMi00NmExLTg5MmMtNTFlYTJlNWY5YTdmXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2708\ufe0f Mach 10 Darkstar cockpit sonic boom across canyon",
            "emotional": "\ud83c\udf05 Maverick and Penny riding motorcycle at golden hour"
        },
        "imdb_id": "tt1745960",
        "imdb_url": "https://www.imdb.com/title/tt1745960/",
        "plot": "Set 30 years after its predecessor, it follows Maverick's return to the United States Navy Strike Fighter Tactics Instructor program (also known as U.S. Navy-Fighter Weapons School - \"TOPGUN\"), where he must confront his past as he trains a group of younger pilots, among them the son of Maverick's deceased best friend Lieutenant Nick \"Goose\" Bradshaw, USN.",
        "actors": "Tom Cruise, Jennifer Connelly, Miles Teller",
        "runtime": "130 min",
        "rated": "PG-13",
        "awards": "Won 1 Oscar. 114 wins & 237 nominations total",
        "metascore": "78",
        "imdb_votes": "904,246",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "giXco2jaZ_4",
        "clip_url": "https://www.youtube-nocookie.com/embed/giXco2jaZ_4",
        "clip_title": "Official Trailer \u2014 Mach 10 Sonic Boom & Danger Zone",
        "clip_duration": "2:23",
        "sound_theme": "Roaring Jet Turbines & Classic 80s Rock Lead"
    },
    {
        "id": "m_36",
        "title": "Mad Max: Fury Road",
        "year": 2015,
        "genres": [
            "Action",
            "Adventure",
            "Sci-Fi"
        ],
        "director": "George Miller",
        "rating": 8.1,
        "match_keywords": [
            "desert",
            "war rig",
            "furiosa",
            "v8"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDRkODJhOTgtOTc1OC00NTgzLTk4NjItNDgxZDY4YjlmNDY2XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udd25 Flame-throwing guitar truck in desert supercell storm",
            "emotional": "\ud83d\udca7 Green Place mourning in vast silent sand dunes"
        },
        "imdb_id": "tt1392190",
        "imdb_url": "https://www.imdb.com/title/tt1392190/",
        "plot": "An apocalyptic story set in the furthest reaches of our planet, in a stark desert landscape where humanity is broken, and almost everyone is crazed fighting for the necessities of life. Within this world exist two rebels on the run who just might be able to restore order. There's Max, a man of action and a man of few words, who seeks peace of mind following the loss of his wife and child in the aftermath of the chaos. And Furiosa, a woman of action and a woman who believes her path to survival may be achieved if she can make it across the desert back to her childhood homeland.",
        "actors": "Tom Hardy, Charlize Theron, Nicholas Hoult",
        "runtime": "120 min",
        "rated": "R",
        "awards": "Won 6 Oscars. 245 wins & 234 nominations total",
        "metascore": "90",
        "imdb_votes": "1,198,396",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "hEJnMQG9ev8",
        "clip_url": "https://www.youtube-nocookie.com/embed/hEJnMQG9ev8",
        "clip_title": "Mad Max: Fury Road - Official Main Trailer",
        "clip_duration": "2:40",
        "sound_theme": "Thunderous Taiko War Drums & Heavy Metal Distortion"
    },
    {
        "id": "m_37",
        "title": "Gladiator",
        "year": 2000,
        "genres": [
            "Action",
            "Drama",
            "Adventure"
        ],
        "director": "Ridley Scott",
        "rating": 8.5,
        "match_keywords": [
            "rome",
            "colosseum",
            "general",
            "revenge"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYWQ4YmNjYjEtOWE1Zi00Y2U4LWI4NTAtMTU0MjkxNWQ1ZmJiXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2694\ufe0f Maximus chariot battle against tigers in Colosseum",
            "emotional": "\ud83c\udf3e Hand brushing golden wheat field in Elysium"
        },
        "imdb_id": "tt0172495",
        "imdb_url": "https://www.imdb.com/title/tt0172495/",
        "plot": "Maximus is a powerful Roman general, loved by the people and the aging Emperor, Marcus Aurelius. Before his death, the Emperor chooses Maximus to be his heir over his own son, Commodus, and a power struggle leaves Maximus and his family condemned to death. The powerful general is captured and put into the Gladiator games until he dies. The only desire that fuels him now is the chance to rise to the top so that he will be able to look into the eyes of the man who will feel his revenge.",
        "actors": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
        "runtime": "155 min",
        "rated": "R",
        "awards": "Won 5 Oscars. 61 wins & 105 nominations total",
        "metascore": "67",
        "imdb_votes": "1,844,518",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "owK1qxDselE",
        "clip_url": "https://www.youtube-nocookie.com/embed/owK1qxDselE",
        "clip_title": "Official Trailer \u2014 Are You Not Entertained? & Now We Are Free",
        "clip_duration": "2:28",
        "sound_theme": "Lisa Gerrard Mournful Vocals & Roman Battle Horns"
    },
    {
        "id": "m_38",
        "title": "The Batman",
        "year": 2022,
        "genres": [
            "Action",
            "Crime",
            "Drama"
        ],
        "director": "Matt Reeves",
        "rating": 7.8,
        "match_keywords": [
            "riddler",
            "gotham",
            "detective",
            "batmobile"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMmU5NGJlMzAtMGNmOC00YjJjLTgyMzUtNjAyYmE4Njg5YWMyXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83e\udd87 Upside down walk toward burning Batmobile highway wreckage",
            "emotional": "\ud83d\udca1 Holding red flare leading flooded stadium survivors"
        },
        "imdb_id": "tt1877830",
        "imdb_url": "https://www.imdb.com/title/tt1877830/",
        "plot": "Two years of nights have turned Bruce Wayne into a nocturnal animal. But as he continues to find his way as Gotham's dark knight, Bruce is forced into a game of cat and mouse with his biggest threat so far, a manic killer known as \"The Riddler\" who is filled with rage and determined to expose the corrupt system whilst picking off all of Gotham's key political figures. Working with both established and new allies, Bruce must track down the killer and see him brought to justice, while investigating his father's true legacy and questioning the effect that he has had on Gotham so far as \"The Batman.\"",
        "actors": "Robert Pattinson, Zo\u00eb Kravitz, Jeffrey Wright",
        "runtime": "176 min",
        "rated": "PG-13",
        "awards": "Nominated for 3 Oscars. 40 wins & 176 nominations total",
        "metascore": "72",
        "imdb_votes": "923,764",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "mqqft2x_Aa4",
        "clip_url": "https://www.youtube-nocookie.com/embed/mqqft2x_Aa4",
        "clip_title": "Main Trailer \u2014 The Bat & Something In The Way",
        "clip_duration": "2:38",
        "sound_theme": "Nirvana Grunge Strings & Menacing Low Brass"
    },
    {
        "id": "m_39",
        "title": "Avengers: Endgame",
        "year": 2019,
        "genres": [
            "Action",
            "Adventure",
            "Sci-Fi"
        ],
        "director": "Anthony & Joe Russo",
        "rating": 8.4,
        "match_keywords": [
            "thanos",
            "portals",
            "avengers assemble",
            "infinity stones"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMWEyNDM2ZmQtMmFkNi00MTQ1LTk1MjItMzdlZGJlYmIyYzZlXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udee1\ufe0f Cap catching Mjolnir with lightning thunderstrike",
            "emotional": "\ud83c\udf0c I Love You 3000 hologram tribute in lakeside cabin"
        },
        "imdb_id": "tt4154796",
        "imdb_url": "https://www.imdb.com/title/tt4154796/",
        "plot": "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos's actions and undo the chaos to the universe, no matter what consequences may be in store, and no matter who they face...",
        "actors": "Robert Downey Jr., Chris Evans, Mark Ruffalo",
        "runtime": "181 min",
        "rated": "PG-13",
        "awards": "Nominated for 1 Oscar. 71 wins & 132 nominations total",
        "metascore": "78",
        "imdb_votes": "1,485,583",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "TcMBFSGVi1c",
        "clip_url": "https://www.youtube-nocookie.com/embed/TcMBFSGVi1c",
        "clip_title": "Official Trailer \u2014 Whatever It Takes & Avengers Theme",
        "clip_duration": "2:26",
        "sound_theme": "Alan Silvestri Avengers Theme & Heartbeat Pulse"
    },
    {
        "id": "m_40",
        "title": "Drive",
        "year": 2011,
        "genres": [
            "Action",
            "Drama",
            "Crime"
        ],
        "director": "Nicolas Winding Refn",
        "rating": 7.8,
        "match_keywords": [
            "getaway",
            "scorpion",
            "synthwave",
            "elevator"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTFmNTFlOTAtNzEyNi00MWU2LTg3MGEtYjA2NWY3MDliNjlkXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\ude97 Night getaway Chevy Malibu cruising under LA streetlights",
            "emotional": "\ud83d\udc8b Slow-motion elevator kiss under warm amber glow"
        },
        "imdb_id": "tt0780504",
        "imdb_url": "https://www.imdb.com/title/tt0780504/",
        "plot": "This action drama follows a mysterious man who has multiple jobs as a garage mechanic, a Hollywood stuntman and a getaway driver seems to be trying to escape his shady past as he falls for his neighbor - whose husband is in prison and who's looking after her child alone. Meanwhile, his garage mechanic boss is trying to set up a race team using gangland money, which implicates our driver as he is to be used as the race team's main driver. Our hero gets more than he bargained for when he meets the man who is married to the woman he loves.",
        "actors": "Ryan Gosling, Carey Mulligan, Bryan Cranston",
        "runtime": "100 min",
        "rated": "R",
        "awards": "Nominated for 1 Oscar. 79 wins & 180 nominations total",
        "metascore": "79",
        "imdb_votes": "761,197",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "KBiOF3y1W0Y",
        "clip_url": "https://www.youtube-nocookie.com/embed/KBiOF3y1W0Y",
        "clip_title": "Official Trailer \u2014 Nightcall & Kavinsky Synthwave",
        "clip_duration": "2:32",
        "sound_theme": "80s Synthwave Neon Arpeggios & Deep Analog Bass"
    },
    {
        "id": "m_68",
        "title": "Mission: Impossible - Fallout",
        "year": 2018,
        "genres": [
            "Action",
            "Adventure",
            "Thriller"
        ],
        "director": "Christopher McQuarrie",
        "rating": 7.7,
        "match_keywords": [
            "ethan hunt",
            "halo jump",
            "helicopter",
            "syndicate"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZmUwZTg2YmMtMmZjOS00ZDYwLWI2ZDgtZDcyY2ZmMWMwZDdlXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\ude81 Helicopter chase clinging to cargo rope over snowy peaks",
            "emotional": "\u26a1 HALO jump through Paris lightning storm"
        },
        "imdb_id": "tt4912910",
        "imdb_url": "https://www.imdb.com/title/tt4912910/",
        "plot": "Two years after Ethan Hunt had successfully captured Solomon Lane, the remnants of the Syndicate have reformed into another organization called the Apostles. Under the leadership of a mysterious fundamentalist known only as John Lark, the organization is planning on acquiring three plutonium cores. Ethan and his team are sent to Berlin to intercept them, but the mission fails when Ethan saves Luther and the Apostles escape with the plutonium. With CIA agent August Walker joining the team, Ethan and his allies must now find the plutonium cores before it's too late.",
        "actors": "Tom Cruise, Henry Cavill, Ving Rhames",
        "runtime": "147 min",
        "rated": "PG-13",
        "awards": "Nominated for 1 BAFTA Award. 26 wins & 42 nominations total",
        "metascore": "87",
        "imdb_votes": "419,025",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "wb49-oV0F78",
        "clip_url": "https://www.youtube-nocookie.com/embed/wb49-oV0F78",
        "clip_title": "Official Trailer \u2014 Halo Jump & Lalo Schifrin Fuse",
        "clip_duration": "2:31",
        "sound_theme": "Fast 5/4 Time Signature Brass & Bongos"
    },
    {
        "id": "m_69",
        "title": "Kill Bill: Vol. 1",
        "year": 2003,
        "genres": [
            "Action",
            "Crime",
            "Drama"
        ],
        "director": "Quentin Tarantino",
        "rating": 8.2,
        "match_keywords": [
            "katana",
            "the bride",
            "revenge",
            "yellow tracksuit"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZmMyYzJlZmYtY2I3NC00NjAyLTkyZWItZjdjZDI1YTYyYTEwXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udde1\ufe0f Crazy 88 sword showdown in House of Blue Leaves",
            "emotional": "\u2744\ufe0f Snow garden duel against O-Ren Ishii"
        },
        "imdb_id": "tt0266697",
        "imdb_url": "https://www.imdb.com/title/tt0266697/",
        "plot": "Four years after taking a bullet in the head at her own wedding, The Bride emerges from a coma and decides it's time for payback... with a vengeance. Having been gunned down by her former boss Bill and his deadly squad of international assassins, it's a kill-or-be-killed fight she didn't start, but is determined to finish.",
        "actors": "Uma Thurman, David Carradine, Daryl Hannah",
        "runtime": "111 min",
        "rated": "R",
        "awards": "Nominated for 5 BAFTA Awards. 30 wins & 103 nominations total",
        "metascore": "69",
        "imdb_votes": "1,305,508",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "7kSuas6mRpk",
        "clip_url": "https://www.youtube-nocookie.com/embed/7kSuas6mRpk",
        "clip_title": "Official Teaser \u2014 Hattori Hanzo Sword & Battle Without Honor",
        "clip_duration": "2:16",
        "sound_theme": "Tomoyasu Hotei Horn Fanfare & Whistling Melody"
    },
    {
        "id": "m_70",
        "title": "Casino Royale",
        "year": 2006,
        "genres": [
            "Action",
            "Adventure",
            "Thriller"
        ],
        "director": "Martin Campbell",
        "rating": 8.0,
        "match_keywords": [
            "james bond",
            "poker",
            "montenegro",
            "vesper"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMWQ1ZDM4NDktMWY0NC00MjcxLWJlMDMtNmE2MGVhYzRjMWQ0XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udfc3 Construction crane freerunning chase in Madagascar",
            "emotional": "\ud83d\udebf James comforting Vesper under shower in hotel room"
        },
        "imdb_id": "tt0381061",
        "imdb_url": "https://www.imdb.com/title/tt0381061/",
        "plot": "James Bond (Daniel Craig) goes on his first mission as a 00. Le Chiffre (Mads Mikkelsen) is a banker to the world's terrorists. He is participating in a poker game at Montenegro, where he must win back his money, in order to stay safe amongst the terrorist market. The boss of MI6, known simply as \"M\" (Dame Judi Dench) sends Bond, along with Vesper Lynd Eva Green) to attend this game and prevent Le Chiffre from winning. Bond, using help from Felix Leiter (Jeffrey Wright), Rene Mathis (Giancarlo Giannini), and having Vesper pose as his partner, enters the most important poker game in his already dangerous career. But if Bond defeats Le Chiffre, will he and Vesper Lynd remain safe?",
        "actors": "Daniel Craig, Eva Green, Judi Dench",
        "runtime": "144 min",
        "rated": "PG-13",
        "awards": "Won 1 BAFTA Award28 wins & 44 nominations total",
        "metascore": "80",
        "imdb_votes": "739,664",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "36mnx8dBbGE",
        "clip_url": "https://www.youtube-nocookie.com/embed/36mnx8dBbGE",
        "clip_title": "Official Trailer \u2014 You Know My Name & Aston Martin Chase",
        "clip_duration": "2:27",
        "sound_theme": "Chris Cornell Gritty Bond Guitar & Brass Stabs"
    },
    {
        "id": "m_71",
        "title": "Heat",
        "year": 1995,
        "genres": [
            "Action",
            "Crime",
            "Drama"
        ],
        "director": "Michael Mann",
        "rating": 8.3,
        "match_keywords": [
            "heist",
            "pacino",
            "de niro",
            "los angeles"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTkxYjU1OTMtYWViZC00ZjAzLWI3MDktZGQ2N2VmMjVjNDRlXkEyXkFqcGc@._V1_QL75_UY562_CR6,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udca5 Historic bank heist street shootout in downtown LA",
            "emotional": "\u2615 Pacino and De Niro sharing coffee table confession"
        },
        "imdb_id": "tt0113277",
        "imdb_url": "https://www.imdb.com/title/tt0113277/",
        "plot": "Hunters and their prey--Neil and his professional criminal crew hunt to score big money targets (banks, vaults, armored cars) and are, in turn, hunted by Lt. Vincent Hanna and his team of cops in the Robbery/Homicide police division. A botched job puts Hanna onto their trail while they regroup and try to put together one last big 'retirement' score. Neil and Vincent are similar in many ways, including their troubled personal lives. At a crucial moment in his life, Neil disobeys the dictum taught to him long ago by his criminal mentor--'Never have anything in your life that you can't walk out on in thirty seconds flat, if you spot the heat coming around the corner'--as he falls in love. Thus the stage is set for the suspenseful ending....",
        "actors": "Al Pacino, Robert De Niro, Val Kilmer",
        "runtime": "170 min",
        "rated": "R",
        "awards": "15 nominations total",
        "metascore": "76",
        "imdb_votes": "800,903",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "0xbBLJ1WGwQ",
        "clip_url": "https://www.youtube-nocookie.com/embed/0xbBLJ1WGwQ",
        "clip_title": "Official Trailer \u2014 Downtown LA Shootout & Elliot Goldenthal",
        "clip_duration": "2:22",
        "sound_theme": "Ambient Urban Crime Guitar & Echoing Snares"
    },
    {
        "id": "m_16",
        "title": "La La Land",
        "year": 2016,
        "genres": [
            "Romance",
            "Comedy",
            "Drama",
            "Music"
        ],
        "director": "Damien Chazelle",
        "rating": 8.0,
        "match_keywords": [
            "jazz",
            "hollywood",
            "tap dance",
            "audition"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udc83 Mia and Sebastian tap dancing overlooking purple LA twilight",
            "emotional": "\ud83c\udfb9 Planetarium waltz floating into starry cosmos"
        },
        "imdb_id": "tt3783958",
        "imdb_url": "https://www.imdb.com/title/tt3783958/",
        "plot": "Aspiring actress serves lattes to movie stars in between auditions and jazz musician Sebastian scrapes by playing cocktail-party gigs in dingy bars. But as success mounts, they are faced with decisions that fray the fragile fabric of their love affair, and the dreams they worked so hard to maintain in each other threaten to rip them apart.",
        "actors": "Ryan Gosling, Emma Stone, Rosemarie DeWitt",
        "runtime": "128 min",
        "rated": "PG-13",
        "awards": "Won 6 Oscars. 246 wins & 313 nominations total",
        "metascore": "94",
        "imdb_votes": "759,966",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "0pdqf4P9MB8",
        "clip_url": "https://www.youtube-nocookie.com/embed/0pdqf4P9MB8",
        "clip_title": "Official Trailer \u2014 City of Stars & Another Day of Sun",
        "clip_duration": "2:25",
        "sound_theme": "Jazz Tap Rhythm & Whistled Piano Waltz"
    },
    {
        "id": "m_17",
        "title": "Crazy Rich Asians",
        "year": 2018,
        "genres": [
            "Romance",
            "Comedy",
            "Drama"
        ],
        "director": "Jon M. Chu",
        "rating": 7.0,
        "match_keywords": [
            "singapore",
            "wedding",
            "glamour",
            "family"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTYxNDMyOTAxN15BMl5BanBnXkFtZTgwMDg1ODYzNTM@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udc8d Glamorous water aisle wedding ceremony in Singapore",
            "emotional": "\ud83c\udc04 Rachel and Eleanor Mahjong showdown at tea house"
        },
        "imdb_id": "tt3104988",
        "imdb_url": "https://www.imdb.com/title/tt3104988/",
        "plot": "Rachel Chu, an American-born Chinese NYU professor, travels with her boyfriend, Nick to his hometown of Singapore for his best friend's wedding. Before long, his secret is out: Nick's family is wealthy, and he's considered the most eligible bachelor in Asia. Every single woman is incredibly jealous of Rachel and wants to bring her down.",
        "actors": "Constance Wu, Henry Golding, Michelle Yeoh",
        "runtime": "120 min",
        "rated": "PG-13",
        "awards": "14 wins & 70 nominations total",
        "metascore": "74",
        "imdb_votes": "207,456",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "ZQ-YX-5bAs0",
        "clip_url": "https://www.youtube-nocookie.com/embed/ZQ-YX-5bAs0",
        "clip_title": "Official Trailer \u2014 Can't Help Falling In Love & Singapore Night",
        "clip_duration": "2:24",
        "sound_theme": "Lush Orchestral Strings & Chinese Jazz Pop"
    },
    {
        "id": "m_18",
        "title": "About Time",
        "year": 2013,
        "genres": [
            "Romance",
            "Comedy",
            "Drama",
            "Fantasy"
        ],
        "director": "Richard Curtis",
        "rating": 7.8,
        "match_keywords": [
            "time travel",
            "london",
            "father son",
            "rain wedding"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTA1ODUzMDA3NzFeQTJeQWpwZ15BbWU3MDgxMTYxNTk@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\ude87 Running through London tube stations in montage",
            "emotional": "\ud83c\udf27\ufe0f Walking through torrential red dress rain wedding"
        },
        "imdb_id": "tt2194499",
        "imdb_url": "https://www.imdb.com/title/tt2194499/",
        "plot": "At the age of 21, Tim Lake (Domhnall Gleeson) discovers he can travel in time... The night after another unsatisfactory New Year party, Tim's father (Bill Nighy) tells his son that the men in his family have always had the ability to travel through time. Tim can't change history, but he can change what happens and has happened in his own life-so he decides to make his world a better place...by getting a girlfriend. Sadly, that turns out not to be as easy as you might think. Moving from the Cornwall coast to London to train as a lawyer, Tim finally meets the beautiful but insecure Mary (Rachel McAdams). They fall in love, then an unfortunate time-travel incident means he's never met her at all. So they meet for the first time again-and again-but finally, after a lot of cunning time-traveling, he wins her heart. Tim then uses his power to create the perfect romantic proposal, to save his wedding from the worst best-man speeches, to save his best friend from professional disaster and to get his pregnant wife to the hospital in time for the birth of their daughter, despite a nasty traffic jam outside Abbey Road. But as his unusual life progresses, Tim finds out that his unique gift can't save him from the sorrows and ups and downs that affect all families, everywhere. There are great limits to what time travel can achieve, and it can be dangerous too.",
        "actors": "Domhnall Gleeson, Rachel McAdams, Bill Nighy",
        "runtime": "123 min",
        "rated": "R",
        "awards": "3 wins & 9 nominations total",
        "metascore": "55",
        "imdb_votes": "429,483",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "7OIFdWk83no",
        "clip_url": "https://www.youtube-nocookie.com/embed/7OIFdWk83no",
        "clip_title": "Official Trailer \u2014 How Long Will I Love You & Time Travel",
        "clip_duration": "2:32",
        "sound_theme": "Warm Acoustic Fingerpicking & Sweet Melodic Cello"
    },
    {
        "id": "m_19",
        "title": "Palm Springs",
        "year": 2020,
        "genres": [
            "Romance",
            "Comedy",
            "Sci-Fi"
        ],
        "director": "Max Barbakow",
        "rating": 7.4,
        "match_keywords": [
            "time loop",
            "wedding",
            "desert",
            "pool float"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BY2VkNGY0MTMtMjEzZi00OThkLWJiOTMtNGU4ZGNjZDE5ZGIyXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83e\udd96 Inflatable dinosaur dancing across desert pool party",
            "emotional": "\u2728 Sitting by campfire accepting endless loop together"
        },
        "imdb_id": "tt9484998",
        "imdb_url": "https://www.imdb.com/title/tt9484998/",
        "plot": "While stuck at a wedding in Palm Springs, Nyles (Andy Samberg) meets Sarah (Cristin Milioti), the maid of honor and family black sheep. After he rescues her from a disastrous toast, Sarah becomes drawn to Nyles and his offbeat nihilism. But when their impromptu tryst is thwarted by a surreal interruption, Sarah must join Nyles in embracing the idea that nothing really matters, and they begin wreaking spirited havoc on the wedding celebration.",
        "actors": "Andy Samberg, Cristin Milioti, J.K. Simmons",
        "runtime": "90 min",
        "rated": "R",
        "awards": "16 wins & 43 nominations total",
        "metascore": "83",
        "imdb_votes": "208,998",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "CpBLtXduh_k",
        "clip_url": "https://www.youtube-nocookie.com/embed/CpBLtXduh_k",
        "clip_title": "Palm Springs - Trailer (Official) | Hulu",
        "clip_duration": "2:28",
        "sound_theme": "Indie Surf Rock Guitars & Upbeat 80s Synth Pop"
    },
    {
        "id": "m_20",
        "title": "(500) Days of Summer",
        "year": 2009,
        "genres": [
            "Romance",
            "Comedy",
            "Drama"
        ],
        "director": "Marc Webb",
        "rating": 7.7,
        "match_keywords": [
            "architecture",
            "ikea",
            "expectations vs reality",
            "autumn"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTk5MjM4OTU1OV5BMl5BanBnXkFtZTcwODkzNDIzMw@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udd7a You Make My Dreams flash mob musical dance in city park",
            "emotional": "\ud83e\ude91 Playing house in IKEA showroom living room"
        },
        "imdb_id": "tt1022603",
        "imdb_url": "https://www.imdb.com/title/tt1022603/",
        "plot": "After it looks as if she's left his life for good this time, Tom Hansen reflects back on the just over one year that he knew Summer Finn. For Tom, it was love at first sight when she walked into the greeting card company where he worked, she the new administrative assistant. Soon, Tom knew that Summer was the woman with whom he wanted to spend the rest of his life. Although Summer did not believe in relationships or boyfriends - in her assertion, real life will always ultimately get in the way - Tom and Summer became more than just friends. Through the trials and tribulations of Tom and Summer's so-called relationship, Tom could always count on the advice of his two best friends, McKenzie and Paul. However, it is Tom's adolescent sister, Rachel, who is his voice of reason. After all is said and done, Tom is the one who ultimately has to make the choice to listen or not.",
        "actors": "Zooey Deschanel, Joseph Gordon-Levitt, Geoffrey Arend",
        "runtime": "95 min",
        "rated": "PG-13",
        "awards": "17 wins & 58 nominations total",
        "metascore": "76",
        "imdb_votes": "613,237",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "PsD0NpFSADM",
        "clip_url": "https://www.youtube-nocookie.com/embed/PsD0NpFSADM",
        "clip_title": "Official Trailer \u2014 Us by Regina Spektor & Split Screen",
        "clip_duration": "2:25",
        "sound_theme": "Quirky Staccato Piano & Folk Pop Harmony"
    },
    {
        "id": "m_21",
        "title": "When Harry Met Sally...",
        "year": 1989,
        "genres": [
            "Romance",
            "Comedy",
            "Drama"
        ],
        "director": "Rob Reiner",
        "rating": 7.7,
        "match_keywords": [
            "friends",
            "new york",
            "delicatessen",
            "autumn central park"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjE0ODEwNjM2NF5BMl5BanBnXkFtZTcwMjU2Mzg3NA@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83e\udd6a I'll have what she's having deli scene",
            "emotional": "\ud83c\udf42 Strolling through golden autumn leaves in Central Park"
        },
        "imdb_id": "tt0098635",
        "imdb_url": "https://www.imdb.com/title/tt0098635/",
        "plot": "Harry and Sally meet when she gives him a ride to New York after they both graduate from the University of Chicago. The film jumps through their lives as they both search for love, but fail, bumping into each other time and time again. Finally a close friendship blooms between them, and they both like having a friend of the opposite sex. But then they are confronted with the problem: \"Can a man and a woman be friends, without sex getting in the way?\"",
        "actors": "Billy Crystal, Meg Ryan, Carrie Fisher",
        "runtime": "95 min",
        "rated": "R",
        "awards": "Nominated for 1 Oscar. 6 wins & 19 nominations total",
        "metascore": "76",
        "imdb_votes": "269,982",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "-E10AcydCuk",
        "clip_url": "https://www.youtube-nocookie.com/embed/-E10AcydCuk",
        "clip_title": "When Harry Met Sally (1989) - Official Trailer",
        "clip_duration": "2:12",
        "sound_theme": "New York Big Band Jazz & Muted Trumpet Swing"
    },
    {
        "id": "m_22",
        "title": "Past Lives",
        "year": 2023,
        "genres": [
            "Romance",
            "Drama"
        ],
        "director": "Celine Song",
        "rating": 7.9,
        "match_keywords": [
            "in-yun",
            "childhood sweetheart",
            "seoul",
            "new york ferry"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjQyMTNhNjUtN2VmYy00NWRhLTkwOTctMGVmNTBmNDIxYjZhXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\uddfd Crossing New York harbor on ferry at sunset",
            "emotional": "\ud83d\ude95 Waiting silently for the Uber under streetlights at 4 AM"
        },
        "imdb_id": "tt13238346",
        "imdb_url": "https://www.imdb.com/title/tt13238346/",
        "plot": "In Korea, Na Young, a girl and Hae Sung, a boy are school mates and good friends. They often walk back home together after school. Na Young moves to Canada and then to New York with her parents. Hae Sung continues living in Korea, does his engineering course, goes through a short spell of military service and then takes up a job. Both keep in touch periodically through video chats where they talk of their past and general stuff. Meanwhile in New York, Na has changed her name to Nora, made a name as a playwright and is happily married to Arthur, an American. Hae is keen to meet Nora and visits her in New York where he spends some time with her and Arthur. What has the future in store for Nora and Hae in their relationship?",
        "actors": "Greta Lee, Teo Yoo, John Magaro",
        "runtime": "105 min",
        "rated": "PG-13",
        "awards": "Nominated for 2 Oscars. 83 wins & 240 nominations total",
        "metascore": "94",
        "imdb_votes": "171,844",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "kA244xewjcI",
        "clip_url": "https://www.youtube-nocookie.com/embed/kA244xewjcI",
        "clip_title": "Past Lives | Official Trailer HD | A24",
        "clip_duration": "2:23",
        "sound_theme": "Gentle Felt Piano & Shimmering Korean Melancholy"
    },
    {
        "id": "m_23",
        "title": "Before Sunset",
        "year": 2004,
        "genres": [
            "Romance",
            "Drama"
        ],
        "director": "Richard Linklater",
        "rating": 8.1,
        "match_keywords": [
            "paris",
            "reunion",
            "bookstore",
            "nine years"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ1MjAwNTM5Ml5BMl5BanBnXkFtZTYwNDM0MTc3._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udee5\ufe0f Cruising down Seine river in late afternoon golden haze",
            "emotional": "\ud83c\udfb8 Baby you're gonna miss that plane waltz in Paris flat"
        },
        "imdb_id": "tt0381681",
        "imdb_url": "https://www.imdb.com/title/tt0381681/",
        "plot": "Early thirty-something American Jesse Wallace is in a Paris bookstore, the last stop on a tour to promote his best selling book, This Time. Although he is vague to reporters about the source material for the book, it is about his chance encounter nine years earlier on June 15-16, 1994 with a Parisienne named Celine, and the memorable and romantic day and evening they spent together in Vienna. At the end of their encounter at the Vienna train station, which is also how the book ends, they, not providing contact information to the other, vowed to meet each other again in exactly six months at that very spot. As the media scrum at the bookstore nears its conclusion, Jesse spots Celine in the crowd, she who only found out about the book when she earlier saw his photograph promoting this public appearance. Much like their previous encounter, Jesse and Celine, who is now an environmental activist, decide to spend time together until he is supposed to catch his flight back to New York, this time only being about an hour. Beyond the issue of the six month meeting, what has happened in their lives in the intervening nine years, and their current lives, they once again talk about their philosophies of life and love, this time with the knowledge of their day together and how it shaped what has happened to them.",
        "actors": "Ethan Hawke, Julie Delpy, Vernon Dobtcheff",
        "runtime": "80 min",
        "rated": "R",
        "awards": "Nominated for 1 Oscar. 10 wins & 32 nominations total",
        "metascore": "91",
        "imdb_votes": "309,299",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "oI3UuneLcyU",
        "clip_url": "https://www.youtube-nocookie.com/embed/oI3UuneLcyU",
        "clip_title": "Official Trailer \u2014 A Waltz For A Night & Paris Promenade",
        "clip_duration": "2:05",
        "sound_theme": "French Gypsy Guitar & Soft Parisian Accordion"
    },
    {
        "id": "m_41",
        "title": "Crazy, Stupid, Love.",
        "year": 2011,
        "genres": [
            "Comedy",
            "Drama",
            "Romance"
        ],
        "director": "Glenn Ficarra",
        "rating": 7.4,
        "match_keywords": [
            "makeover",
            "dirty dancing",
            "soulmate",
            "ryan gosling"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTg2MjkwMTM0NF5BMl5BanBnXkFtZTcwMzc4NDg2NQ@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udf27\ufe0f The iconic Dirty Dancing lift in the pouring rain",
            "emotional": "\ud83d\udc8d Backyard fight turning into family reconciliation speech"
        },
        "imdb_id": "tt1570728",
        "imdb_url": "https://www.imdb.com/title/tt1570728/",
        "plot": "Cal (Steve Carell) and Emily (Julianne Moore) have the perfect life together living the American dream... until Emily asks for a divorce. Now Cal, Mr Husband, has to navigate the single scene with a little help from his professional bachelor friend Jacob Palmer (Ryan Gosling). Make that a lot of help...",
        "actors": "Steve Carell, Ryan Gosling, Julianne Moore",
        "runtime": "118 min",
        "rated": "PG-13",
        "awards": "5 wins & 23 nominations total",
        "metascore": "68",
        "imdb_votes": "601,291",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "8iCwtxJejik",
        "clip_url": "https://www.youtube-nocookie.com/embed/8iCwtxJejik",
        "clip_title": "Official Trailer \u2014 Rain Scene & The Black Keys",
        "clip_duration": "2:26",
        "sound_theme": "Punchy Pop Funk Drums & Smooth RnB Grooves"
    },
    {
        "id": "m_42",
        "title": "The Notebook",
        "year": 2004,
        "genres": [
            "Drama",
            "Romance"
        ],
        "director": "Nick Cassavetes",
        "rating": 7.8,
        "match_keywords": [
            "letters",
            "rain kiss",
            "memory",
            "first love"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjE0ZjgzMzYtMTAxYi00NGMzLThmZDktNzFlMzA2MWRmYWQ0XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udea3 Rowboat surrounded by white swans in rain thunderstorm",
            "emotional": "\ud83d\udcd6 Reading old notebook memories in sunlit nursing home"
        },
        "imdb_id": "tt0332280",
        "imdb_url": "https://www.imdb.com/title/tt0332280/",
        "plot": "With almost religious devotion, Duke, a kind octogenarian inmate of a peaceful nursing home, reads daily a captivating story from the worn-out pages of his leather-bound notebook to a fellow female patient. To keep her company, Duke recounts the fascinating love affair between impecunious but poetic country boy Noah and Allie, an affluent city girl. And little by little, Duke unfolds a Southern, lumber-scented summer romance beneath the tall trees of late 1930s North Carolina. Indeed, it seems as if the silent manuscript possesses the unfathomable power to penetrate the opaque clouds that enclose the silver-haired dame; slowly but surely, the enchanted lady becomes immersed in the strangely alluring fairy tale of the young ardent lovers' highs and lows. But nobody knows what tomorrow holds. Are all summer loves doomed to fail?",
        "actors": "Gena Rowlands, James Garner, Rachel McAdams",
        "runtime": "123 min",
        "rated": "PG-13",
        "awards": "12 wins & 10 nominations total",
        "metascore": "53",
        "imdb_votes": "686,952",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "BjJcYdEOI0k",
        "clip_url": "https://www.youtube-nocookie.com/embed/BjJcYdEOI0k",
        "clip_title": "The Notebook (2004) Official Trailer",
        "clip_duration": "2:22",
        "sound_theme": "Soaring Cinematic Cello & Romantic Piano Crescendo"
    },
    {
        "id": "m_43",
        "title": "Notting Hill",
        "year": 1999,
        "genres": [
            "Comedy",
            "Drama",
            "Romance"
        ],
        "director": "Roger Michell",
        "rating": 7.2,
        "match_keywords": [
            "bookstore",
            "actress",
            "london",
            "press conference"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjY3YWI5OTMtYTdlNy00ZTZiLWEwYjItN2M1MGVkMDM4ZDExXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\ude97 Rushing across London traffic to Ritz press conference",
            "emotional": "\ud83d\udeaa Just a girl standing in front of a boy asking him to love her"
        },
        "imdb_id": "tt0125439",
        "imdb_url": "https://www.imdb.com/title/tt0125439/",
        "plot": "Every man's dream comes true for William Thacker, an unsuccessful Notting Hill bookstore owner, when Anna Scott, the world's most beautiful woman and best-liked actress, enters his shop. A little later, he still can't believe it himself, William runs into her again - this time spilling orange juice over her. Anna accepts his offer to change in his nearby apartment, and thanks him with a kiss, which seems to surprise her even more than him. Eventually, Anna and William get to know each other better over the months, but being together with the world's most wanted woman is not easy - neither around your closest friends, nor in front of the all-devouring press.",
        "actors": "Hugh Grant, Julia Roberts, Richard McCabe",
        "runtime": "124 min",
        "rated": "PG-13",
        "awards": "Won 1 BAFTA Award11 wins & 17 nominations total",
        "metascore": "68",
        "imdb_votes": "380,809",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "4RI0QvaGoiI",
        "clip_url": "https://www.youtube-nocookie.com/embed/4RI0QvaGoiI",
        "clip_title": "Official Trailer \u2014 She & When You Say Nothing At All",
        "clip_duration": "2:18",
        "sound_theme": "Warm British Pop Acoustic & Soft Vocal Hum"
    },
    {
        "id": "m_44",
        "title": "Pride & Prejudice",
        "year": 2005,
        "genres": [
            "Drama",
            "Romance"
        ],
        "director": "Joe Wright",
        "rating": 7.8,
        "match_keywords": [
            "darcy",
            "elizabeth",
            "estate",
            "rain proposal"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTA1NDQ3NTcyOTNeQTJeQWpwZ15BbWU3MDA0MzA4MzE@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udfdb\ufe0f Intense rain confrontation under temple stone portico",
            "emotional": "\ud83c\udf05 Darcy walking across misty sunrise meadow towards Lizzie"
        },
        "imdb_id": "tt0414387",
        "imdb_url": "https://www.imdb.com/title/tt0414387/",
        "plot": "The story is based on Jane Austen's novel about five sisters - Jane (Rosamund Pike), Elizabeth (Keira Knightley), Mary (Talulah Riley), Kitty (Carey Mulligan), and Lydia Bennet (Jena Malone) - in Georgian England. Their lives are turned upside down when wealthy young Mr. Bingley (Simon Woods) and his best friend, Mr. Darcy (Matthew Macfadyen), arrive in their neighborhood.",
        "actors": "Keira Knightley, Matthew Macfadyen, Brenda Blethyn",
        "runtime": "129 min",
        "rated": "PG",
        "awards": "Nominated for 4 Oscars. 13 wins & 59 nominations total",
        "metascore": "82",
        "imdb_votes": "368,401",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "1dYv5u6v55Y",
        "clip_url": "https://www.youtube-nocookie.com/embed/1dYv5u6v55Y",
        "clip_title": "Official Trailer \u2014 Dawn & Dario Marianelli Solo Piano",
        "clip_duration": "2:28",
        "sound_theme": "Romantic Piano Arpeggios & English Countryside Strings"
    },
    {
        "id": "m_45",
        "title": "Before Sunrise",
        "year": 1995,
        "genres": [
            "Drama",
            "Romance"
        ],
        "director": "Richard Linklater",
        "rating": 8.1,
        "match_keywords": [
            "vienna",
            "train",
            "conversation",
            "listening booth"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDZhZmI1ZTUtYWI3NC00NTMwLTk3NWMtNDc0OGNjM2I0ZjlmXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udfa0 Walking along Danube canal in Vienna at midnight",
            "emotional": "\ud83c\udfa7 Stolen glances in vintage vinyl record listening booth"
        },
        "imdb_id": "tt0112471",
        "imdb_url": "https://www.imdb.com/title/tt0112471/",
        "plot": "American tourist Jesse and French student Celine meet by chance on the train from Budapest to Vienna. Sensing that they are developing a connection, Jesse asks Celine to spend the day with him in Vienna, and she agrees. So they pass the time before his scheduled flight the next morning together. How do two perfect strangers connect so intimately over the course of a single day? What is that special thing that bonds two people so strongly? As their bond turns to love, what will happen to them the next morning when Jesse flies away?",
        "actors": "Ethan Hawke, Julie Delpy, Andrea Eckert",
        "runtime": "101 min",
        "rated": "R",
        "awards": "2 wins & 7 nominations total",
        "metascore": "79",
        "imdb_votes": "373,558",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "6MUcuqbGTxc",
        "clip_url": "https://www.youtube-nocookie.com/embed/6MUcuqbGTxc",
        "clip_title": "Before Sunrise (1995) Trailer",
        "clip_duration": "2:01",
        "sound_theme": "Folk Singer-Songwriter Guitar & European Train Drone"
    },
    {
        "id": "m_46",
        "title": "Midnight in Paris",
        "year": 2011,
        "genres": [
            "Comedy",
            "Fantasy",
            "Romance"
        ],
        "director": "Woody Allen",
        "rating": 7.7,
        "match_keywords": [
            "1920s",
            "hemingway",
            "fitzgerald",
            "peugeot"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTM4NjY1MDQwMl5BMl5BanBnXkFtZTcwNTI3Njg3NA@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udd70\ufe0f Vintage Peugeot midnight time travel ride through alleys",
            "emotional": "\u2614 Walking in Parisian rain along Seine river without umbrella"
        },
        "imdb_id": "tt1605783",
        "imdb_url": "https://www.imdb.com/title/tt1605783/",
        "plot": "Gil and Inez travel to Paris as a tag-along vacation on her parents' business trip. Gil is a successful Hollywood writer but is struggling on his first novel. He falls in love with the city and thinks he and Inez should move there after they get married, but Inez does not share his romantic notions of the city or the idea that the 1920s were the golden age. When Inez goes off dancing with her friends, Gil takes a walk at midnight and discovers what could be the ultimate source of inspiration for writing. Gil's daily walks at midnight in Paris could take him closer to the heart of the city but further from the woman he's about to marry.",
        "actors": "Owen Wilson, Rachel McAdams, Kathy Bates",
        "runtime": "94 min",
        "rated": "PG-13",
        "awards": "Won 1 Oscar. 26 wins & 103 nominations total",
        "metascore": "81",
        "imdb_votes": "469,474",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "BYRWfS2s2v4",
        "clip_url": "https://www.youtube-nocookie.com/embed/BYRWfS2s2v4",
        "clip_title": "Official Trailer \u2014 Si Tu Vois Ma M\u00e8re & Midnight Bell",
        "clip_duration": "2:09",
        "sound_theme": "Sidney Bechet Jazz Clarinet & Vintage Paris Swing"
    },
    {
        "id": "m_47",
        "title": "Silver Linings Playbook",
        "year": 2012,
        "genres": [
            "Comedy",
            "Drama",
            "Romance"
        ],
        "director": "David O. Russell",
        "rating": 7.7,
        "match_keywords": [
            "dance competition",
            "parlay",
            "philadelphia",
            "letter"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTM2MTI5NzA3MF5BMl5BanBnXkFtZTcwODExNTc0OA@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udc83 Chaotic high-energy ballroom dance routine finale",
            "emotional": "\ud83d\udc8c Reading the real letter in the Philadelphia winter snow"
        },
        "imdb_id": "tt1045658",
        "imdb_url": "https://www.imdb.com/title/tt1045658/",
        "plot": "Against medical advice and without the knowledge of her husband Pat Solatano Sr., caring Dolores Solatano discharges her adult son, Pat Solatano Jr., from a Maryland mental health institution after his minimum eight-month court ordered stint. The condition of the release includes Pat Jr. moving back in with his parents in their Philadelphia home. Although Pat Jr.'s institutionalization was due to him beating up the lover of his wife Nikki, he was diagnosed with bipolar disorder. Nikki has since left him and has received a restraining order against him. Although he is on medication (which he doesn't take because of the way it makes him feel) and has mandatory therapy sessions, Pat Jr. feels like he can manage on the outside solely by healthy living and looking for the \"silver linings\" in his life. His goals are to get his old job back as a substitute teacher, but more importantly reunite with Nikki. He finds there are certain instances where he doesn't cope well; however, no less so than some others who have never been institutionalized, such as his Philadelphia Eagles obsessed father who has resorted to being a bookie to earn a living, his best friend Ronnie who quietly seethes over the control wielded by his wife Veronica, and Veronica's widowed sister, Tiffany Maxwell, a girl with problems of her own. In their fragile mental states, Pat Jr. and Tiffany embark on a love/hate friendship based primarily on what help the other can provide in achieving their individual goals. But they may reevaluate their goals as their relationship progresses.",
        "actors": "Bradley Cooper, Jennifer Lawrence, Robert De Niro",
        "runtime": "122 min",
        "rated": "R",
        "awards": "Won 1 Oscar. 90 wins & 148 nominations total",
        "metascore": "81",
        "imdb_votes": "770,744",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "Lj5_FhLaaQQ",
        "clip_url": "https://www.youtube-nocookie.com/embed/Lj5_FhLaaQQ",
        "clip_title": "Official Trailer \u2014 Dance Audition & Stevie Wonder",
        "clip_duration": "2:30",
        "sound_theme": "Uplifting Motown Funk & Warm Acoustic Guitar Chords"
    },
    {
        "id": "m_48",
        "title": "Me Before You",
        "year": 2016,
        "genres": [
            "Drama",
            "Romance"
        ],
        "director": "Thea Sharrock",
        "rating": 7.4,
        "match_keywords": [
            "castle",
            "bumblebee tights",
            "paris",
            "wheelchair"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ2NjE4NDE2NV5BMl5BanBnXkFtZTgwOTcwNDE5NzE@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udff0 Wheelchair dance at country wedding in red dress",
            "emotional": "\u2615 Reading final letter at Parisian outdoor caf\u00e9"
        },
        "imdb_id": "tt2674426",
        "imdb_url": "https://www.imdb.com/title/tt2674426/",
        "plot": "Lou Clark knows lots of things. She knows how many footsteps there are between the bus stop and home. She knows she likes working in The Buttered Bun tea shop and she knows she might not love her boyfriend Patrick. What Lou doesn't know is she's about to lose her job or that knowing what's coming is what keeps her sane. Will Traynor knows a road accident took away his desire to live. He knows everything feels very small and rather joyless now and he knows exactly how he's going to put a stop to that. What Will doesn't know is that Lou is about to burst into his world in a riot of color. And neither of them knows they're going to change each other for all time.",
        "actors": "Emilia Clarke, Sam Claflin, Janet McTeer",
        "runtime": "110 min",
        "rated": "PG-13",
        "awards": "6 wins & 6 nominations total",
        "metascore": "51",
        "imdb_votes": "330,388",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "Eh993__rOxA",
        "clip_url": "https://www.youtube-nocookie.com/embed/Eh993__rOxA",
        "clip_title": "Official Trailer \u2014 Photograph by Ed Sheeran & Castle Walk",
        "clip_duration": "2:27",
        "sound_theme": "Emotional Ed Sheeran Acoustic Ballad & Strings"
    },
    {
        "id": "m_72",
        "title": "Am\u00e9lie",
        "year": 2001,
        "genres": [
            "Comedy",
            "Romance"
        ],
        "director": "Jean-Pierre Jeunet",
        "rating": 8.3,
        "match_keywords": [
            "montmartre",
            "photobooth",
            "paris",
            "creme brulee"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTNmYzY0MWQtZGZmNy00Y2Y4LWFmMDQtMTZjYTdiYzEwZGQ2XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udef5 Moped ride through sunlit cobblestones of Montmartre",
            "emotional": "\ud83e\udd44 Cracking golden sugar crust on cr\u00e8me br\u00fbl\u00e9e with spoon"
        },
        "imdb_id": "tt0211915",
        "imdb_url": "https://www.imdb.com/title/tt0211915/",
        "plot": "Young Am\u00e9lie Poulain works in a Paris caf\u00e9, lives alone, and surreptitiously helps people. Whether it's secretly returning the childhood treasures of a middle-aged man or matchmaking for the lovelorn, Am\u00e9lie gives fate a helping hand. Her world takes a new, exciting turn when she meets Nino.",
        "actors": "Audrey Tautou, Mathieu Kassovitz, Rufus",
        "runtime": "122 min",
        "rated": "R",
        "awards": "Nominated for 5 Oscars. 60 wins & 74 nominations total",
        "metascore": "70",
        "imdb_votes": "839,094",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "HUECWi5pX7o",
        "clip_url": "https://www.youtube-nocookie.com/embed/HUECWi5pX7o",
        "clip_title": "Official Trailer \u2014 Comptine d'un autre \u00e9t\u00e9 & Accordion",
        "clip_duration": "2:10",
        "sound_theme": "Yann Tiersen Toy Piano & French Accordion Chimes"
    },
    {
        "id": "m_73",
        "title": "10 Things I Hate About You",
        "year": 1999,
        "genres": [
            "Comedy",
            "Drama",
            "Romance"
        ],
        "director": "Gil Junger",
        "rating": 7.3,
        "match_keywords": [
            "heath ledger",
            "guitar",
            "can't take my eyes off you",
            "high school"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTQwYmRhNGQtODI2Mi00ZTRlLTk0Y2QtY2NkNjE1MGNhNTgwXkEyXkFqcGc@._V1_QL75_UX380_CR0,1,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfa4 Heath Ledger singing on high school stadium bleachers",
            "emotional": "\ud83d\udcdd Reading 10 things emotional poem in literature class"
        },
        "imdb_id": "tt0147800",
        "imdb_url": "https://www.imdb.com/title/tt0147800/",
        "plot": "Adapted from William Shakespeare's play \"The Taming of the Shrew,\" 10 Things I Hate About You starts off with Cameron, new student at Padua High, sitting in the office of the quirky guidance counselor Ms. Perky. He is then shown around the school by Michael, who will become his best friend. During his tour is when Cameron first sees Bianca Stratford, a beautiful sophomore with one problem: she isn't allowed to date. And neither is her \"shrew\" sister, Katarina, a senior who loves indie rock and feminist prose and hates conformity. But Kat and Bianca's father alters his house rule: now, Bianca can date... as long as Kat has a date, too. Now, in order for Cameron to date Bianca, he has to find someone to date Kat. So Michael helps him enlist the help of pretty-boy/jerk/model Joey Donner, tricking him into thinking that *he* will get to take Bianca out if he pays someone to take out Kat. His choice: Patrick Verona, a bad-boy with a mysterious reputation--some say he ate a live duck once, others that he lit a state trooper on fire, and even more claim that he had a brief porn career. Will Patrick win Kat's heart? Will Cameron win Bianca's? Or will everything hit the fan...?",
        "actors": "Heath Ledger, Julia Stiles, Joseph Gordon-Levitt",
        "runtime": "97 min",
        "rated": "PG-13",
        "awards": "2 wins & 13 nominations total",
        "metascore": "70",
        "imdb_votes": "448,378",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "Ax8qnxP2TWY",
        "clip_url": "https://www.youtube-nocookie.com/embed/Ax8qnxP2TWY",
        "clip_title": "10 Things I Hate About You (1999) Trailer",
        "clip_duration": "2:15",
        "sound_theme": "90s Alt-Rock Electric Guitar & Funky Bass Line"
    },
    {
        "id": "m_74",
        "title": "Titanic",
        "year": 1997,
        "genres": [
            "Drama",
            "Romance"
        ],
        "director": "James Cameron",
        "rating": 7.9,
        "match_keywords": [
            "ship",
            "iceberg",
            "heart of the ocean",
            "flying on bow"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzYyN2FiZmUtYWYzMy00MzViLWJkZTMtOGY1ZjgzNWMwN2YxXkEyXkFqcGc@._V1_QL75_UX380_CR0,2,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udea2 Massive bow cutting through Atlantic sunset with dolphin pods",
            "emotional": "\ud83c\udf0a Jack and Rose arms outstretched: I'm flying!"
        },
        "imdb_id": "tt0120338",
        "imdb_url": "https://www.imdb.com/title/tt0120338/",
        "plot": "84 years later, a 100 year-old woman named Rose DeWitt Bukater tells the story to her granddaughter Lizzy Calvert, Brock Lovett, Lewis Bodine, Bobby Buell and Anatoly Mikailavich on the Keldysh about her life set in April 10th 1912, on a ship called Titanic when young Rose boards the departing ship with the upper-class passengers and her mother, Ruth DeWitt Bukater, and her fianc\u00e9, Caledon Hockley. Meanwhile, a drifter and artist named Jack Dawson and his best friend Fabrizio De Rossi win third-class tickets to the ship in a game. And she explains the whole story from departure until the death of Titanic on its first and last voyage April 15th, 1912 at 2:20 in the morning.",
        "actors": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "runtime": "194 min",
        "rated": "PG-13",
        "awards": "Won 11 Oscars. 126 wins & 84 nominations total",
        "metascore": "75",
        "imdb_votes": "1,389,357",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "kVrqfYjkTdQ",
        "clip_url": "https://www.youtube-nocookie.com/embed/kVrqfYjkTdQ",
        "clip_title": "Official Trailer \u2014 My Heart Will Go On & James Horner Flute",
        "clip_duration": "2:33",
        "sound_theme": "Irish Uilleann Pipes & Epic Orchestral Swell"
    },
    {
        "id": "m_07",
        "title": "Oppenheimer",
        "year": 2023,
        "genres": [
            "Biography",
            "Drama",
            "History"
        ],
        "director": "Christopher Nolan",
        "rating": 8.9,
        "match_keywords": [
            "physics",
            "manhattan project",
            "trinity test",
            "atomic"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2JkMDc5MGQtZjg3YS00NmFiLWIyZmQtZTJmNTM5MjVmYTQ4XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udca5 Blinding silent flash of the Trinity test fireball",
            "emotional": "\ud83c\udf27\ufe0f Rain drops causing ripples on pond reflecting future atomic age"
        },
        "imdb_id": "tt15398776",
        "imdb_url": "https://www.imdb.com/title/tt15398776/",
        "plot": "A dramatization of the life story of J. Robert Oppenheimer, the physicist who had a large hand in the development of the atomic bomb, thus helping end World War 2. We see his life from university days all the way to post-WW2, where his fame saw him embroiled in political machinations.",
        "actors": "Cillian Murphy, Emily Blunt, Matt Damon",
        "runtime": "180 min",
        "rated": "R",
        "awards": "Won 7 Oscars. 370 wins & 378 nominations total",
        "metascore": "90",
        "imdb_votes": "1,024,033",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "uYPbbksJxIg",
        "clip_url": "https://www.youtube-nocookie.com/embed/uYPbbksJxIg",
        "clip_title": "Official Trailer \u2014 Can You Hear The Music & Ludwig Violin",
        "clip_duration": "3:06",
        "sound_theme": "Accelerating 24-BPM Violin Staccato & Atomic Rumble"
    },
    {
        "id": "m_08",
        "title": "Pulp Fiction",
        "year": 1994,
        "genres": [
            "Crime",
            "Drama"
        ],
        "director": "Quentin Tarantino",
        "rating": 8.9,
        "match_keywords": [
            "non linear",
            "diner",
            "briefcase",
            "dance contest"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTViYTE3ZGQtNDBlMC00ZTAyLTkyODMtZGRiZDg0MjA2YThkXkEyXkFqcGc@._V1_QL75_UY562_CR3,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udd7a Jack Rabbit Slims twist dance contest to Chuck Berry",
            "emotional": "\ud83d\udcbc Glowing golden light emanating from the mysterious briefcase"
        },
        "imdb_id": "tt0110912",
        "imdb_url": "https://www.imdb.com/title/tt0110912/",
        "plot": "Jules Winnfield (Samuel L. Jackson) and Vincent Vega (John Travolta) are two hitmen who are out to retrieve a suitcase stolen from their employer, mob boss Marsellus Wallace (Ving Rhames). Wallace has also asked Vincent to take his wife Mia (Uma Thurman) out a few days later when Wallace himself will be out of town. Butch Coolidge (Bruce Willis) is an aging boxer who is paid by Wallace to lose his fight. The lives of these seemingly unrelated people are woven together comprising of a series of funny, bizarre and uncalled-for incidents.",
        "actors": "John Travolta, Uma Thurman, Samuel L. Jackson",
        "runtime": "154 min",
        "rated": "R",
        "awards": "Won 1 Oscar. 69 wins & 72 nominations total",
        "metascore": "95",
        "imdb_votes": "2,431,656",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "s7EdQ4FqbhY",
        "clip_url": "https://www.youtube-nocookie.com/embed/s7EdQ4FqbhY",
        "clip_title": "Official Trailer \u2014 Misirlou & You Never Can Tell",
        "clip_duration": "2:26",
        "sound_theme": "Dick Dale Surf Rock Tremolo Guitar & Horn Riffs"
    },
    {
        "id": "m_09",
        "title": "Parasite",
        "year": 2019,
        "genres": [
            "Drama",
            "Thriller",
            "Comedy"
        ],
        "director": "Bong Joon-ho",
        "rating": 8.5,
        "match_keywords": [
            "class divide",
            "basement",
            "peach",
            "rain flood"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjk1Y2U4MjQtY2ZiNS00OWQyLWI3MmYtZWUwNmRjYWRiNWNhXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udf27\ufe0f Escaping down endless Seoul concrete stairs in torrential storm",
            "emotional": "\u26fa Pitching glowing yellow tent on manicured rainy lawn"
        },
        "imdb_id": "tt6751668",
        "imdb_url": "https://www.imdb.com/title/tt6751668/",
        "plot": "The Kims - mother and father Chung-sook and Ki-taek, and their young adult offspring, son Ki-woo and daughter Ki-jung - are a poor family living in a shabby and cramped half basement apartment in a busy lower working class commercial district of Seoul. Without even knowing it, they, especially Mr. and Mrs. Kim, literally smell of poverty. Often as a collective, they perpetrate minor scams to get by, and even when they have jobs, they do the minimum work required. Ki-woo is the one who has dreams of getting out of poverty by one day going to university. Despite not having that university education, Ki-woo is chosen by his university student friend Min, who is leaving to go to school, to take over his tutoring job to Park Da-hye, who Min plans to date once he returns to Seoul and she herself is in university. The Parks are a wealthy family who for four years have lived in their modernistic house designed by and the former residence of famed architect Namgoong. While Mr. and Mrs. Park are all about status, Mrs. Park has a flighty, simpleminded mentality and temperament, which Min tells Ki-woo to feel comfortable in lying to her about his education to get the job. In getting the job, Ki-woo further learns that Mrs. Park is looking for an art therapist for the Parks' adolescent son, Da-song, Ki-woo quickly recommending his professional art therapist friend \"Jessica\", really Ki-jung who he knows can pull off the scam in being the easiest liar of the four Kims. In Ki-woo also falling for Da-hye, he begins to envision himself in that house, and thus the Kims as a collective start a plan for all the Kims, like Ki-jung using assumed names, to replace existing servants in the Parks' employ in orchestrating reasons for them to be fired. The most difficult to get rid of may be Moon-gwang, the Parks' housekeeper who literally came with the house - she Namgoong's housekeeper when he lived there - and thus knows all the little nooks and crannies of it better than the Parks themselves. The question then becomes how far the Kims can take this scam in their quest to become their version of the Parks.",
        "actors": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "runtime": "132 min",
        "rated": "R",
        "awards": "Won 4 Oscars. 309 wins & 261 nominations total",
        "metascore": "97",
        "imdb_votes": "1,148,210",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "isOGD_7hNIY",
        "clip_url": "https://www.youtube-nocookie.com/embed/isOGD_7hNIY",
        "clip_title": "PARASITE - Official Trailer",
        "clip_duration": "2:16",
        "sound_theme": "Classical Baroque Cello & Tragicomic String Plucks"
    },
    {
        "id": "m_10",
        "title": "Whiplash",
        "year": 2014,
        "genres": [
            "Drama",
            "Music"
        ],
        "director": "Damien Chazelle",
        "rating": 8.5,
        "match_keywords": [
            "drums",
            "tempo",
            "jazz",
            "caravan"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDFjOWFkYzktYzhhMC00NmYyLTkwY2EtYjViMDhmNzg0OGFkXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83e\udd41 Blistering blood on cymbals Caravan drum solo climax",
            "emotional": "\ud83d\udc40 Mutual nod of respect between Andrew and Fletcher"
        },
        "imdb_id": "tt2582802",
        "imdb_url": "https://www.imdb.com/title/tt2582802/",
        "plot": "Nineteen year old Andrew Niemann wants to be the greatest jazz drummer in the world, in a league with Buddy Rich. This goal is despite not coming from a pedigree of greatest, musical or otherwise, with Jim, his high school teacher father, being a failed writer. Andrew is starting his first year at Shaffer Conservatory of Music, the best music school in the United States. At Shaffer, being the best means being accepted to study under Terence Fletcher and being asked to play in his studio band, which represents the school at jazz competitions. Based on their less than positive first meeting, Andrew is surprised that Fletcher asks him to join the band, albeit in the alternate drummer position which he is more than happy to do initially. Andrew quickly learns that Fletcher operates on fear and intimidation, never settling for what he considers less than the best each and every time. Being the best in Fletcher's mind does not only entail playing well, but knowing that you're playing well and if not what you're doing wrong. His modus operandi creates an atmosphere of fear and of every man or woman for him/herself within the band. Regardless, Andrew works hard to be the best. He has to figure out his life priorities and what he is willing to sacrifice to be the best. The other question becomes how much emotional abuse he will endure by Fletcher to reach that greatness, which he may believe he can only achieve with the avenues opened up by Fletcher.",
        "actors": "Miles Teller, J.K. Simmons, Melissa Benoist",
        "runtime": "106 min",
        "rated": "R",
        "awards": "Won 3 Oscars. 100 wins & 144 nominations total",
        "metascore": "89",
        "imdb_votes": "1,134,459",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "7d_jQycdQGo",
        "clip_url": "https://www.youtube-nocookie.com/embed/7d_jQycdQGo",
        "clip_title": "Official Trailer \u2014 Caravan & Fletcher Double Time Swing",
        "clip_duration": "2:28",
        "sound_theme": "Blistering Fast Jazz Drums & Big Band Brass Stabs"
    },
    {
        "id": "m_49",
        "title": "The Godfather",
        "year": 1972,
        "genres": [
            "Crime",
            "Drama"
        ],
        "director": "Francis Ford Coppola",
        "rating": 9.2,
        "match_keywords": [
            "corleone",
            "mafia",
            "cannoli",
            "don"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNGEwYjgwOGQtYjg5ZS00Njc1LTk2ZGEtM2QwZWQ2NjdhZTE5XkEyXkFqcGc@._V1_QL75_UY562_CR8,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udd2b Restaurant baptism assassination montage across NY",
            "emotional": "\ud83d\udeaa Closing door on Kay as Michael is kissed Don Corleone"
        },
        "imdb_id": "tt0068646",
        "imdb_url": "https://www.imdb.com/title/tt0068646/",
        "plot": "The Godfather \"Don\" Vito Corleone is the head of the Corleone mafia family in New York. He is at the event of his daughter's wedding. Michael, Vito's youngest son and a decorated WWII Marine is also present at the wedding. Michael seems to be uninterested in being a part of the family business. Vito is a powerful man, and is kind to all those who give him respect but is ruthless against those who do not. But when a powerful and treacherous rival wants to sell drugs and needs the Don's influence for the same, Vito refuses to do it. What follows is a clash between Vito's fading old values and the new ways which may cause Michael to do the thing he was most reluctant in doing and wage a mob war against all the other mafia families which could tear the Corleone family apart.",
        "actors": "Marlon Brando, Al Pacino, James Caan",
        "runtime": "175 min",
        "rated": "R",
        "awards": "Won 3 Oscars. 31 wins & 31 nominations total",
        "metascore": "100",
        "imdb_votes": "2,222,804",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "UaVTIH8mujA",
        "clip_url": "https://www.youtube-nocookie.com/embed/UaVTIH8mujA",
        "clip_title": "Official 50th Anniv Trailer \u2014 Nino Rota Speak Softly Love",
        "clip_duration": "2:22",
        "sound_theme": "Mournful Sicilian Mandolin & Trumpet Solitary Melody"
    },
    {
        "id": "m_50",
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genres": [
            "Drama"
        ],
        "director": "Frank Darabont",
        "rating": 9.3,
        "match_keywords": [
            "prison",
            "escape",
            "hope",
            "pacific"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf27\ufe0f Andy Dufresne arms outstretched in pouring rain",
            "emotional": "\ud83c\udf0a Red walking along blue Zihuatanejo beach to embrace Andy"
        },
        "imdb_id": "tt0111161",
        "imdb_url": "https://www.imdb.com/title/tt0111161/",
        "plot": "Chronicles the experiences of a formerly successful banker as a prisoner in the gloomy jailhouse of Shawshank after being found guilty of a crime he did not commit. The film portrays the man's unique way of dealing with his new, torturous life; along the way he befriends a number of fellow prisoners, most notably a wise long-term inmate named Red.",
        "actors": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "runtime": "142 min",
        "rated": "R",
        "awards": "Nominated for 7 Oscars. 21 wins & 43 nominations total",
        "metascore": "82",
        "imdb_votes": "3,235,958",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "PLl99DlL6b4",
        "clip_url": "https://www.youtube-nocookie.com/embed/PLl99DlL6b4",
        "clip_title": "Official Trailer \u2014 Brooks Was Here & Thomas Newman Piano",
        "clip_duration": "2:11",
        "sound_theme": "Hopeful Ambient Piano Chords & Soaring String Section"
    },
    {
        "id": "m_51",
        "title": "Fight Club",
        "year": 1999,
        "genres": [
            "Drama",
            "Thriller"
        ],
        "director": "David Fincher",
        "rating": 8.8,
        "match_keywords": [
            "soap",
            "tyler durden",
            "rules",
            "buildings"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTgyOGQ1NDItNGU3Ny00MjU3LTg2YWEtNmEyYjBiMjI1Y2M5XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udca5 Skyscraper demolition fireworks finale across skyline",
            "emotional": "\ud83e\udd1d Holding hands as city financial buildings collapse"
        },
        "imdb_id": "tt0137523",
        "imdb_url": "https://www.imdb.com/title/tt0137523/",
        "plot": "A nameless first-person narrator attends support groups in an attempt to subdue his emotional state and relieve his insomniac state. When he meets Marla, another fake attendee of support groups, his life seems to become a little more bearable. However, when he associates himself with Tyler he is dragged into an underground fight club and soap-making scheme. Together the two men spiral out of control and engage in competitive rivalry for love and power.",
        "actors": "Brad Pitt, Edward Norton, Meat Loaf",
        "runtime": "139 min",
        "rated": "R",
        "awards": "Nominated for 1 Oscar. 12 wins & 38 nominations total",
        "metascore": "67",
        "imdb_votes": "2,601,857",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "qtRKdVHc-cE",
        "clip_url": "https://www.youtube-nocookie.com/embed/qtRKdVHc-cE",
        "clip_title": "Fight Club (1999) Trailer",
        "clip_duration": "2:25",
        "sound_theme": "Industrial Lo-Fi Breakbeats & Pixies Dreamy Vocals"
    },
    {
        "id": "m_52",
        "title": "The Wolf of Wall Street",
        "year": 2013,
        "genres": [
            "Biography",
            "Comedy",
            "Crime"
        ],
        "director": "Martin Scorsese",
        "rating": 8.2,
        "match_keywords": [
            "stocks",
            "ipo",
            "yacht",
            "jordan belfort"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\ude81 White Ferrari crawl to country club scene",
            "emotional": "\ud83c\udfa4 Sell me this pen convention seminar speech"
        },
        "imdb_id": "tt0993846",
        "imdb_url": "https://www.imdb.com/title/tt0993846/",
        "plot": "Jordan Belfort (DiCaprio) is Long Island penny stockbroker who serves almost two years in prison for refusing to co-operate in a huge 1990s securities fraud case that involved widespread corruption on Wall Street and in the corporate banking world, including mob infiltration.",
        "actors": "Leonardo DiCaprio, Jonah Hill, Margot Robbie",
        "runtime": "180 min",
        "rated": "R",
        "awards": "Nominated for 5 Oscars. 38 wins & 180 nominations total",
        "metascore": "75",
        "imdb_votes": "1,784,314",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "iszwuX1AK6A",
        "clip_url": "https://www.youtube-nocookie.com/embed/iszwuX1AK6A",
        "clip_title": "Official Trailer \u2014 Black Skinhead & Chest Thump",
        "clip_duration": "2:21",
        "sound_theme": "Heavy Kanye Tribal Beats & Matthew McConaughey Thump"
    },
    {
        "id": "m_53",
        "title": "Goodfellas",
        "year": 1990,
        "genres": [
            "Biography",
            "Crime",
            "Drama"
        ],
        "director": "Martin Scorsese",
        "rating": 8.7,
        "match_keywords": [
            "mob",
            "copacabana",
            "heist",
            "funny how"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2E5NzI2ZGMtY2VjNi00YTRjLWI1MDUtZGY5OWU1MWJjZjRjXkEyXkFqcGc@._V1_QL75_UX380_CR0,3,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udeaa Steadicam kitchen entrance to Copacabana front row table",
            "emotional": "\ud83c\udf5d Sunday sauce prison dinner prep slicing garlic with razor"
        },
        "imdb_id": "tt0099685",
        "imdb_url": "https://www.imdb.com/title/tt0099685/",
        "plot": "Henry Hill recounts his life in the mob, from his teenage years to his eventual downfall. Immersed in organized crime, he experiences wealth, power, and violence alongside friends Jimmy Conway and Tommy DeVito. The film blends crime, drama, and dark humor, exploring loyalty, ambition, betrayal, and the consequences of criminal life. Themes of family, morality, and the fleeting nature of power underpin the story.",
        "actors": "Robert De Niro, Ray Liotta, Joe Pesci",
        "runtime": "145 min",
        "rated": "R",
        "awards": "Won 1 Oscar. 44 wins & 38 nominations total",
        "metascore": "92",
        "imdb_votes": "1,388,009",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "2ilzidi_J8Q",
        "clip_url": "https://www.youtube-nocookie.com/embed/2ilzidi_J8Q",
        "clip_title": "Official Trailer \u2014 Layla Piano Exit & Tony Bennett",
        "clip_duration": "2:23",
        "sound_theme": "Classic Derek & the Dominos Rock Piano & Rhythmic Bass"
    },
    {
        "id": "m_54",
        "title": "Se7en",
        "year": 1995,
        "genres": [
            "Crime",
            "Drama",
            "Mystery"
        ],
        "director": "David Fincher",
        "rating": 8.6,
        "match_keywords": [
            "detective",
            "seven deadly sins",
            "box",
            "rain"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTU5MTFlYmItMGI4Ni00OTJkLTlmZTUtNzcyNzcxM2Y4MWI0XkEyXkFqcGdeQXVyNzg5OTk2OA@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udce6 Desert power line delivery sequence at sunset",
            "emotional": "\ud83c\udf27\ufe0f Detectives sharing coffee under torrential city downpour"
        },
        "imdb_id": "tt0114388",
        "imdb_url": "https://www.imdb.com/title/tt0114388/",
        "plot": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives in a perpetually rain-soaked, decaying city.",
        "actors": "Morgan Freeman, Brad Pitt, Kevin Spacey, Gwyneth Paltrow",
        "runtime": "127 min",
        "rated": "R",
        "awards": "Nominated for 1 Oscar. 29 wins & 43 nominations total",
        "metascore": "65",
        "imdb_votes": "15",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "znmZoVkCjpI",
        "clip_url": "https://www.youtube-nocookie.com/embed/znmZoVkCjpI",
        "clip_title": "Official Trailer \u2014 Howard Shore Darkness & Rain Downpour",
        "clip_duration": "2:24",
        "sound_theme": "Menacing Low Brass Growls & Industrial Noise Pulse"
    },
    {
        "id": "m_55",
        "title": "Shutter Island",
        "year": 2010,
        "genres": [
            "Mystery",
            "Thriller",
            "Drama"
        ],
        "director": "Martin Scorsese",
        "rating": 8.2,
        "match_keywords": [
            "ashecliffe",
            "lighthouse",
            "marshals",
            "ward c"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BN2FjNWExYzEtY2YzOC00YjNlLTllMTQtNmIwM2Q1YzBhOWM1XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf2a\ufe0f Hurricane storm surge breaking against lighthouse cliffs",
            "emotional": "\ud83c\udfdb\ufe0f Which would be worse - to live as a monster, or die as a good man?"
        },
        "imdb_id": "tt1130884",
        "imdb_url": "https://www.imdb.com/title/tt1130884/",
        "plot": "In 1954, up-and-coming U.S. marshal Teddy Daniels is assigned to investigate the disappearance of a patient from Boston's Shutter Island Ashecliffe Hospital. He's been pushing for an assignment on the island for personal reasons, but before long he thinks he's been brought there as part of a twisted plot by hospital doctors whose radical treatments range from unethical to illegal to downright sinister. Teddy's shrewd investigating skills soon provide a promising lead, but the hospital refuses him access to records he suspects would break the case wide open. As a hurricane cuts off communication with the mainland, more dangerous criminals \"escape\" in the confusion, and the puzzling, improbable clues multiply, Teddy begins to doubt everything - his memory, his partner, even his own sanity.",
        "actors": "Leonardo DiCaprio, Emily Mortimer, Mark Ruffalo",
        "runtime": "138 min",
        "rated": "R",
        "awards": "11 wins & 66 nominations total",
        "metascore": "63",
        "imdb_votes": "1,644,111",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "5iaYLCiq5RM",
        "clip_url": "https://www.youtube-nocookie.com/embed/5iaYLCiq5RM",
        "clip_title": "Official Trailer \u2014 On The Nature of Daylight & Foghorn",
        "clip_duration": "2:26",
        "sound_theme": "Lush Max Richter Adagio Strings & Foghorn Echoes"
    },
    {
        "id": "m_75",
        "title": "No Country for Old Men",
        "year": 2007,
        "genres": [
            "Crime",
            "Drama",
            "Thriller"
        ],
        "director": "Ethan & Joel Coen",
        "rating": 8.2,
        "match_keywords": [
            "anton chigurh",
            "coin toss",
            "texas",
            "briefcase"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA5Njk3MjM4OV5BMl5BanBnXkFtZTcwMTc5MTE1MQ@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83e\ude99 Gas station coin toss: What's the most you ever lost on a coin toss?",
            "emotional": "\ud83c\udf05 Sheriff Bell recounting his father riding ahead into the snow with fire"
        },
        "imdb_id": "tt0477348",
        "imdb_url": "https://www.imdb.com/title/tt0477348/",
        "plot": "In rural Texas, welder and hunter Llewelyn Moss (Josh Brolin) discovers the remains of several drug runners who have all killed each other in an exchange gone violently wrong. Rather than report the discovery to the police, Moss decides to simply take the two million dollars present for himself. This puts the psychopathic killer, Anton Chigurh (Javier Bardem), on his trail as he dispassionately murders nearly every rival, bystander and even employer in his pursuit of his quarry and the money. As Moss desperately attempts to keep one step ahead, the blood from this hunt begins to flow behind him with relentlessly growing intensity as Chigurh closes in. Meanwhile, the laconic Sheriff Ed Tom Bell (Tommy Lee Jones) blithely oversees the investigation even as he struggles to face the sheer enormity of the crimes he is attempting to thwart.",
        "actors": "Tommy Lee Jones, Javier Bardem, Josh Brolin",
        "runtime": "122 min",
        "rated": "R",
        "awards": "Won 4 Oscars. 165 wins & 139 nominations total",
        "metascore": "92",
        "imdb_votes": "1,177,271",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "38A__WT3-o0",
        "clip_url": "https://www.youtube-nocookie.com/embed/38A__WT3-o0",
        "clip_title": "Official Trailer \u2014 Texas Desert Wind & Minimalist Drone",
        "clip_duration": "2:25",
        "sound_theme": "Eerie Desert Wind Whistle & Sub-Harmonic Low Resonance"
    },
    {
        "id": "m_76",
        "title": "The Departed",
        "year": 2006,
        "genres": [
            "Crime",
            "Drama",
            "Thriller"
        ],
        "director": "Martin Scorsese",
        "rating": 8.5,
        "match_keywords": [
            "undercover",
            "boston",
            "irish mob",
            "mole"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_QL75_UY562_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfe2 Rooftop standoff overlooking Boston state house dome",
            "emotional": "\ud83d\udc00 Gold domed state house window final shot"
        },
        "imdb_id": "tt0407887",
        "imdb_url": "https://www.imdb.com/title/tt0407887/",
        "plot": "In this crime-action tour de force, the South Boston state police force is waging war on Irish-American organized crime. Young undercover cop Billy Costigan is assigned to infiltrate the mob syndicate run by gangland chief Frank Costello. While Billy quickly gains Costello's confidence, Colin Sullivan, a hardened young criminal who has infiltrated the state police as an informer for the syndicate, is rising to a position of power in the Special Investigation Unit. Each man becomes deeply consumed by their double lives, gathering information about the plans and counter-plans of the operations they have penetrated. But when it becomes clear to both the mob and the police that there is a mole in their midst, Billy and Colin are suddenly in danger of being caught and exposed to the enemy - and each must race to uncover the identity of the other man in time to save themselves. But is either willing to turn on their friends and comrades they've made during their long stints undercover?",
        "actors": "Leonardo DiCaprio, Matt Damon, Jack Nicholson",
        "runtime": "151 min",
        "rated": "R",
        "awards": "Won 4 Oscars. 100 wins & 141 nominations total",
        "metascore": "85",
        "imdb_votes": "1,551,506",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "iojhqm0JTW4",
        "clip_url": "https://www.youtube-nocookie.com/embed/iojhqm0JTW4",
        "clip_title": "Official Trailer \u2014 I'm Shipping Up To Boston & Bagpipes",
        "clip_duration": "2:24",
        "sound_theme": "Dropkick Murphys Celtic Punk & Distorted Guitar Riffs"
    },
    {
        "id": "m_77",
        "title": "Taxi Driver",
        "year": 1976,
        "genres": [
            "Crime",
            "Drama"
        ],
        "director": "Martin Scorsese",
        "rating": 8.2,
        "match_keywords": [
            "you talkin to me",
            "new york",
            "mohawk",
            "checker cab"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDNhMGYwM2UtMTdlZS00MGQ1LWI2YzAtODY5YWI1MjYyNzRmXkEyXkFqcGc@._V1_QL75_UX380_CR0,7,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\ude95 Cruising neon lit steaming 1970s Manhattan streets at midnight",
            "emotional": "\ud83e\ude9e You talkin' to me? mirror rehearsal in rundown apartment"
        },
        "imdb_id": "tt0075314",
        "imdb_url": "https://www.imdb.com/title/tt0075314/",
        "plot": "Travis Bickle is an ex-Marine and Vietnam War veteran living in New York City. As he suffers from insomnia, he spends his time working as a taxi driver at night, watching porn movies at seedy cinemas during the day, or thinking about how the world, New York in particular, has deteriorated into a cesspool. He's a loner who has strong opinions about what is right and wrong with mankind. For him, the one bright spot in humanity is Betsy, a worker on the presidential nomination campaign of Senator Charles Palantine. After an incident, he believes he has to do whatever he needs to make the world a better place.",
        "actors": "Robert De Niro, Jodie Foster, Cybill Shepherd",
        "runtime": "114 min",
        "rated": "R",
        "awards": "Nominated for 4 Oscars. 22 wins & 21 nominations total",
        "metascore": "94",
        "imdb_votes": "1,023,905",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "UUxD4-dEzn0",
        "clip_url": "https://www.youtube-nocookie.com/embed/UUxD4-dEzn0",
        "clip_title": "Official Trailer \u2014 Bernard Herrmann Late Night Saxophone",
        "clip_duration": "2:18",
        "sound_theme": "Sensual Dark Jazz Alto Sax & Muffled City Rain"
    },
    {
        "id": "m_11",
        "title": "Spider-Man: Into the Spider-Verse",
        "year": 2018,
        "genres": [
            "Animation",
            "Action",
            "Adventure",
            "Sci-Fi"
        ],
        "director": "Peter Ramsey",
        "rating": 8.4,
        "match_keywords": [
            "multiverse",
            "leap of faith",
            "brooklyn",
            "graffiti"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgzOF5BMl5BanBnXkFtZTgwNTkwNTQ3NjM@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udfd9\ufe0f Upward falling Leap of Faith dive through Brooklyn skyline",
            "emotional": "\ud83c\udfa8 Spray painting What's Up Danger mural under railway arches"
        },
        "imdb_id": "tt4633694",
        "imdb_url": "https://www.imdb.com/title/tt4633694/",
        "plot": "Phil Lord and Christopher Miller, the creative minds behind The Lego Movie and 21 Jump Street, bring their unique talents to a fresh vision of a different Spider-Man Universe, with a groundbreaking visual style that's the first of its kind. \"Spider-Man(TM): Into the Spider-Verse\" introduces Brooklyn teen Miles Morales (Shameik Moore), and the limitless possibilities of the Spider-Verse, where more than one can wear the mask.",
        "actors": "Shameik Moore, Jake Johnson, Hailee Steinfeld",
        "runtime": "117 min",
        "rated": "PG",
        "awards": "Won 1 Oscar. 85 wins & 60 nominations total",
        "metascore": "87",
        "imdb_votes": "777,014",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "tg52up16eq0",
        "clip_url": "https://www.youtube-nocookie.com/embed/tg52up16eq0",
        "clip_title": "Official Trailer \u2014 Sunflower by Post Malone & What's Up Danger",
        "clip_duration": "2:35",
        "sound_theme": "Sun-Drenched Hip-Hop Trap Beats & 808 Bass Glides"
    },
    {
        "id": "m_12",
        "title": "Spirited Away",
        "year": 2001,
        "genres": [
            "Animation",
            "Adventure",
            "Family",
            "Fantasy"
        ],
        "director": "Hayao Miyazaki",
        "rating": 8.6,
        "match_keywords": [
            "bathhouse",
            "no face",
            "chihiro",
            "haku"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTEyNmEwOWUtYzkyOC00ZTQ4LTllZmUtMjk0Y2YwOGUzYjRiXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udc09 Haku white river dragon soaring above spirit world lake",
            "emotional": "\ud83d\ude82 Silent train gliding across endless shallow blue water"
        },
        "imdb_id": "tt0245429",
        "imdb_url": "https://www.imdb.com/title/tt0245429/",
        "plot": "The fanciful adventures of a ten-year-old girl named Chihiro, who discovers a secret world when she and her family get lost and venture through a hillside tunnel. When her parents undergo a mysterious transformation, Chihiro must fend for herself as she encounters strange spirits, assorted creatures and a grumpy sorceress who seeks to prevent her from returning to the human world.",
        "actors": "Miyu Irino, Rumi Hiiragi, Mari Natsuki",
        "runtime": "124 min",
        "rated": "PG",
        "awards": "Won 1 Oscar. 58 wins & 31 nominations total",
        "metascore": "96",
        "imdb_votes": "964,088",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "ByXuk9QqQkk",
        "clip_url": "https://www.youtube-nocookie.com/embed/ByXuk9QqQkk",
        "clip_title": "Official Trailer \u2014 One Summer's Day & Joe Hisaishi Piano",
        "clip_duration": "2:20",
        "sound_theme": "Lyrical Japanese Orchestral Piano & Mystical Bells"
    },
    {
        "id": "m_13",
        "title": "Spider-Man: Across the Spider-Verse",
        "year": 2023,
        "genres": [
            "Animation",
            "Action",
            "Adventure",
            "Sci-Fi"
        ],
        "director": "Kemp Powers",
        "rating": 8.7,
        "match_keywords": [
            "canon event",
            "miguel o'hara",
            "spider-gwen",
            "mumble"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNThiZjA3MjItZGY5Ni00ZmJhLWEwN2EtOTBlYTA4Y2E0M2ZmXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udd78\ufe0f Dimensional Spider-Society chase across futuristic Nueva York",
            "emotional": "\ud83c\udf06 Gwen and Miles sitting upside down on Manhattan skyscraper clock"
        },
        "imdb_id": "tt9362722",
        "imdb_url": "https://www.imdb.com/title/tt9362722/",
        "plot": "Miles Morales returns for the next chapter of the Oscar\u00ae-winning Spider-Verse saga, an epic adventure that will transport Brooklyn's full-time, friendly neighborhood Spider-Man across the Multiverse to join forces with Gwen Stacy and a new team of Spider-People to face off with a villain more powerful than anything they have ever encountered.",
        "actors": "Shameik Moore, Hailee Steinfeld, Brian Tyree Henry",
        "runtime": "140 min",
        "rated": "PG",
        "awards": "Nominated for 1 Oscar. 107 wins & 164 nominations total",
        "metascore": "86",
        "imdb_votes": "509,515",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "cqGjhVJWtEg",
        "clip_url": "https://www.youtube-nocookie.com/embed/cqGjhVJWtEg",
        "clip_title": "Official Trailer \u2014 Metro Boomin Am I Dreaming & 2099 Synth",
        "clip_duration": "2:40",
        "sound_theme": "Futuristic 2099 Trap Beats & Orchestral Glitch Synths"
    },
    {
        "id": "m_14",
        "title": "Ratatouille",
        "year": 2007,
        "genres": [
            "Animation",
            "Comedy",
            "Family",
            "Fantasy"
        ],
        "director": "Brad Bird",
        "rating": 8.1,
        "match_keywords": [
            "paris",
            "chef",
            "remy",
            "critic"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTMzODU0NTkxMF5BMl5BanBnXkFtZTcwMjQ4MzMzMw@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf73 Kitchen brigade whirlwind preparing confit byaldi rush",
            "emotional": "\ud83c\udf45 Anton Ego tasting first bite and flashing back to mother kitchen"
        },
        "imdb_id": "tt0382932",
        "imdb_url": "https://www.imdb.com/title/tt0382932/",
        "plot": "A rat named Remy dreams of becoming a great French chef despite his family's wishes and the obvious problem of being a rat in a decidedly rodent-phobic profession. When fate places Remy in the sewers of Paris, he finds himself ideally situated beneath a restaurant made famous by his culinary hero, Auguste Gusteau. Despite the apparent dangers of being an unlikely, and certainly unwanted, visitor in the kitchen of a fine French restaurant, Remy's passion for cooking soon sets into motion a hilarious and exciting rat race that turns the culinary world of Paris upside down.",
        "actors": "Brad Garrett, Lou Romano, Patton Oswalt",
        "runtime": "111 min",
        "rated": "G",
        "awards": "Won 1 Oscar. 69 wins & 42 nominations total",
        "metascore": "96",
        "imdb_votes": "940,588",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "NgsQ8mVkN8w",
        "clip_url": "https://www.youtube-nocookie.com/embed/NgsQ8mVkN8w",
        "clip_title": "Official Trailer \u2014 Le Festin & Michael Giacchino Paris Waltz",
        "clip_duration": "2:25",
        "sound_theme": "Breezy French Accordion & Jazzy Upright Bass"
    },
    {
        "id": "m_56",
        "title": "Your Name.",
        "year": 2016,
        "genres": [
            "Animation",
            "Drama",
            "Fantasy",
            "Romance"
        ],
        "director": "Makoto Shinkai",
        "rating": 8.4,
        "match_keywords": [
            "comet",
            "body swap",
            "tokyo",
            "twilight"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjI1ODZkYTgtYTY3Yy00ZTJkLWFkOTgtZDUyYWM4MzQwNjk0XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\u2604\ufe0f Tiamat comet splitting into sapphire fragments across night sky",
            "emotional": "\ud83c\udf05 Meeting at Kataware-doki twilight mountain ridge"
        },
        "imdb_id": "tt5311514",
        "imdb_url": "https://www.imdb.com/title/tt5311514/",
        "plot": "Mitsuha is the daughter of the mayor of a small mountain town. She's a straightforward high school girl who lives with her sister and her grandmother and has no qualms about letting it be known that she's uninterested in Shinto rituals or helping her father's electoral campaign. Instead she dreams of leaving the boring town and trying her luck in Tokyo. Taki is a high school boy in Tokyo who works part-time in an Italian restaurant and aspires to become an architect or an artist. Every night he has a strange dream where he becomes...a high school girl in a small mountain town.",
        "actors": "Ry\u00fbnosuke Kamiki, Mone Kamishiraishi, Ryo Narita",
        "runtime": "106 min",
        "rated": "TV-PG",
        "awards": "17 wins & 27 nominations total",
        "metascore": "81",
        "imdb_votes": "385,171",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "xU47nhruN-Q",
        "clip_url": "https://www.youtube-nocookie.com/embed/xU47nhruN-Q",
        "clip_title": "Official Trailer \u2014 Sparkle & Zenzenzense by RADWIMPS",
        "clip_duration": "2:26",
        "sound_theme": "J-Rock Electric Guitars & Emotional Piano Breakdown"
    },
    {
        "id": "m_57",
        "title": "Coco",
        "year": 2017,
        "genres": [
            "Animation",
            "Adventure",
            "Family",
            "Music"
        ],
        "director": "Lee Unkrich",
        "rating": 8.4,
        "match_keywords": [
            "land of the dead",
            "guitar",
            "marigold bridge",
            "remember me"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMDIyM2E2NTAtMzlhNy00ZGUxLWI1NjgtZDY5MzhiMDc5NGU3XkEyXkFqcGc@._V1_QL75_UY562_CR7,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf09 Crossing golden glowing marigold petal bridge into Land of Dead",
            "emotional": "\ud83c\udfb8 Singing Remember Me softly with acoustic guitar to Mama Coco"
        },
        "imdb_id": "tt2380307",
        "imdb_url": "https://www.imdb.com/title/tt2380307/",
        "plot": "Despite his family's baffling generations-old ban on music, Miguel dreams of becoming an accomplished musician like his idol, Ernesto de la Cruz. Desperate to prove his talent, Miguel finds himself in the stunning and colorful Land of the Dead following a mysterious chain of events. Along the way, he meets charming trickster Hector, and together, they set off on an extraordinary journey to unlock the real story behind Miguel's family history.",
        "actors": "Anthony Gonzalez, Gael Garc\u00eda Bernal, Benjamin Bratt",
        "runtime": "105 min",
        "rated": "PG",
        "awards": "Won 2 Oscars. 113 wins & 42 nominations total",
        "metascore": "81",
        "imdb_votes": "704,092",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "Rvr68u6k5sI",
        "clip_url": "https://www.youtube-nocookie.com/embed/Rvr68u6k5sI",
        "clip_title": "Coco Official Final Trailer",
        "clip_duration": "2:27",
        "sound_theme": "Mexican Vihuela Strumming & Brass Mariachi Melodies"
    },
    {
        "id": "m_58",
        "title": "WALL\u00b7E",
        "year": 2008,
        "genres": [
            "Animation",
            "Adventure",
            "Family",
            "Sci-Fi"
        ],
        "director": "Andrew Stanton",
        "rating": 8.4,
        "match_keywords": [
            "robot",
            "earth",
            "plant",
            "space"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjExMTg5OTU0NF5BMl5BanBnXkFtZTcwMjMxMzMzMw@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\ude80 Fire extinguisher dance in zero-gravity starlit space",
            "emotional": "\ud83e\udd1d Solar charging holding hands at sunrise on deserted Earth"
        },
        "imdb_id": "tt0910970",
        "imdb_url": "https://www.imdb.com/title/tt0910970/",
        "plot": "In a distant, but not so unrealistic, future where mankind has abandoned earth because it has become covered with trash from products sold by the powerful multi-national Buy N Large corporation, WALL-E, a garbage collecting robot has been left to clean up the mess. Mesmerized with trinkets of Earth's history and show tunes, WALL-E is alone on Earth except for a sprightly pet cockroach. One day, EVE, a sleek (and dangerous) reconnaissance robot, is sent to Earth to find proof that life is once again sustainable. WALL-E falls in love with EVE. WALL-E rescues EVE from a dust storm and shows her a living plant he found amongst the rubble. Consistent with her \"directive\", EVE takes the plant and automatically enters a deactivated state except for a blinking green beacon. WALL-E, doesn't understand what has happened to his new friend, but, true to his love, he protects her from wind, rain, and lightning, even as she is unresponsive. One day a massive ship comes to reclaim EVE, but WALL-E, out of love or loneliness, hitches a ride on the outside of the ship to rescue EVE. The ship arrives back at a large space cruise ship, which is carrying all of the humans who evacuated Earth 700 years earlier. The people of Earth ride around this space resort on hovering chairs which give them a constant feed of TV and video chatting. They drink all of their meals through a straw out of laziness and/or bone loss, and are all so fat that they can barely move. When the auto-pilot computer, acting on hastily-given instructions sent many centuries before, tries to prevent the people of Earth from returning by stealing the plant, WALL-E, EVE, the portly captain, and a band of broken robots stage a mutiny.",
        "actors": "Ben Burtt, Elissa Knight, Jeff Garlin",
        "runtime": "98 min",
        "rated": "G",
        "awards": "Won 1 Oscar. 96 wins & 95 nominations total",
        "metascore": "95",
        "imdb_votes": "1,306,354",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "CZ1CATNbXg0",
        "clip_url": "https://www.youtube-nocookie.com/embed/CZ1CATNbXg0",
        "clip_title": "WALL-E (2008) Trailer",
        "clip_duration": "2:30",
        "sound_theme": "Classic 60s Musical Brass & Ethereal Space Echoes"
    },
    {
        "id": "m_59",
        "title": "Princess Mononoke",
        "year": 1997,
        "genres": [
            "Animation",
            "Action",
            "Adventure",
            "Fantasy"
        ],
        "director": "Hayao Miyazaki",
        "rating": 8.4,
        "match_keywords": [
            "forest spirit",
            "iron town",
            "wolf",
            "nature"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNjAzODViNGEtMjBkYi00N2U5LWJjNjAtY2U0MGJhZTEwOTU0XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udc3a San riding giant white wolf into Iron Town battle",
            "emotional": "\ud83e\udd8c Forest Spirit footsteps blooming instant flowers & moss"
        },
        "imdb_id": "tt0119698",
        "imdb_url": "https://www.imdb.com/title/tt0119698/",
        "plot": "While protecting his village from rampaging boar-god/demon, a confident young warrior, Ashitaka, is stricken by a deadly curse. To save his life, he must journey to the forests of the west. Once there, he's embroiled in a fierce campaign that humans were waging on the forest. The ambitious Lady Eboshi and her loyal clan use their guns against the gods of the forest and a brave young woman, Princess Mononoke, who was raised by a wolf-god. Ashitaka sees the good in both sides and tries to stem the flood of blood. This is met by animosity by both sides as they each see him as supporting the enemy.",
        "actors": "Y\u00f4ji Matsuda, Yuriko Ishida, Y\u00fbko Tanaka",
        "runtime": "133 min",
        "rated": "PG-13",
        "awards": "14 wins & 6 nominations total",
        "metascore": "78",
        "imdb_votes": "477,867",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "4OiMOHRDs14",
        "clip_url": "https://www.youtube-nocookie.com/embed/4OiMOHRDs14",
        "clip_title": "Official Trailer \u2014 The Legend of Ashitaka & Hisaishi Horns",
        "clip_duration": "2:19",
        "sound_theme": "Epic Japanese Orchestral Horns & Taiko Rhythms"
    },
    {
        "id": "m_60",
        "title": "Howl's Moving Castle",
        "year": 2004,
        "genres": [
            "Animation",
            "Adventure",
            "Family",
            "Fantasy"
        ],
        "director": "Hayao Miyazaki",
        "rating": 8.2,
        "match_keywords": [
            "howl",
            "calcifer",
            "moving castle",
            "magic"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTY1OTg0MjE3MV5BMl5BanBnXkFtZTcwNTUxMTkyMQ@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udff0 Walking on air above colorful European flower village",
            "emotional": "\ud83d\udd25 Sophie feeding bacon to Calcifer dancing hearth fire"
        },
        "imdb_id": "tt0347149",
        "imdb_url": "https://www.imdb.com/title/tt0347149/",
        "plot": "A love story between an 18-year-old girl named Sophie, cursed by a witch into an old woman's body, and a magician named Howl. Under the curse, Sophie sets out to seek her fortune, which takes her to Howl's strange moving castle. In the castle, Sophie meets Howl's fire demon, named Karishif\u00e2. Seeing that she is under a curse, the demon makes a deal with Sophie--if she breaks the contract he is under with Howl, then Karushif\u00e2 will lift the curse that Sophie is under, and she will return to her 18-year-old shape.",
        "actors": "Chieko Baish\u00f4, Takuya Kimura, Tatsuya Gash\u00fbin",
        "runtime": "119 min",
        "rated": "PG",
        "awards": "Nominated for 1 Oscar. 14 wins & 20 nominations total",
        "metascore": "82",
        "imdb_votes": "507,343",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "iwROgK94zcM",
        "clip_url": "https://www.youtube-nocookie.com/embed/iwROgK94zcM",
        "clip_title": "Official Trailer \u2014 Merry-Go-Round of Life & Hisaishi Waltz",
        "clip_duration": "2:18",
        "sound_theme": "Whimsical 3/4 Time Signature Piano & Rich Brass Chords"
    },
    {
        "id": "m_61",
        "title": "Puss in Boots: The Last Wish",
        "year": 2022,
        "genres": [
            "Animation",
            "Action",
            "Adventure",
            "Comedy"
        ],
        "director": "Joel Crawford",
        "rating": 7.8,
        "match_keywords": [
            "death",
            "nine lives",
            "wishing star",
            "whistle"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzg0MWUzMjctYjVlOS00NzVjLWIwZDMtNzg1YzNkYzdjNTMwXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udc3a Wolf spinning twin sickles duel in crystal wishing star ring",
            "emotional": "\ud83d\udc36 Perrito gently resting chin on panicking Puss chest"
        },
        "imdb_id": "tt3915174",
        "imdb_url": "https://www.imdb.com/title/tt3915174/",
        "plot": "When Puss in Boots discovers that his passion for adventure has taken its toll and he has burned through eight of his nine lives, he launches an epic journey to restore them by finding the mythical Last Wish.",
        "actors": "Antonio Banderas, Salma Hayek, Harvey Guill\u00e9n",
        "runtime": "102 min",
        "rated": "PG",
        "awards": "Nominated for 1 Oscar. 8 wins & 57 nominations total",
        "metascore": "73",
        "imdb_votes": "218,530",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "RqrXhwS33yc",
        "clip_url": "https://www.youtube-nocookie.com/embed/RqrXhwS33yc",
        "clip_title": "Puss In Boots: The Last Wish - Official Trailer 2",
        "clip_duration": "2:45",
        "sound_theme": "Chilling Two-Note Whistle & Fast Flamenco Guitar"
    },
    {
        "id": "m_78",
        "title": "Up",
        "year": 2009,
        "genres": [
            "Animation",
            "Adventure",
            "Comedy",
            "Drama"
        ],
        "director": "Pete Docter",
        "rating": 8.3,
        "match_keywords": [
            "balloons",
            "paradise falls",
            "carl and ellie",
            "dug"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNmI1ZTc5MWMtMDYyOS00ZDc2LTkzOTAtNjQ4NWIxNjYyNDgzXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udf88 10,000 colorful helium balloons lifting Victorian house into clouds",
            "emotional": "\ud83d\udcd6 Ellie's Married Life scrapbook page: Thanks for the adventure"
        },
        "imdb_id": "tt1049413",
        "imdb_url": "https://www.imdb.com/title/tt1049413/",
        "plot": "As a boy, Carl Fredricksen wanted to explore South America and find the forbidden Paradise Falls. About 64 years later he gets to begin his journey along with Boy Scout Russell by lifting his house with thousands of balloons. On their journey, they make many new friends including a talking dog, and figure out that someone has evil plans. Carl soon realizes that this evildoer is his childhood idol.",
        "actors": "Edward Asner, Jordan Nagai, John Ratzenberger",
        "runtime": "96 min",
        "rated": "PG",
        "awards": "Won 2 Oscars. 81 wins & 88 nominations total",
        "metascore": "88",
        "imdb_votes": "1,225,827",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "qas5lWp7_R0",
        "clip_url": "https://www.youtube-nocookie.com/embed/qas5lWp7_R0",
        "clip_title": "Official Trailer \u2014 Married Life & Giacchino Trumpet Waltz",
        "clip_duration": "2:21",
        "sound_theme": "Heartwarming Vintage Trumpet Waltz & Toy Percussion"
    },
    {
        "id": "m_79",
        "title": "Suzume",
        "year": 2022,
        "genres": [
            "Animation",
            "Action",
            "Adventure",
            "Fantasy"
        ],
        "director": "Makoto Shinkai",
        "rating": 7.7,
        "match_keywords": [
            "door",
            "keystone",
            "cat chair",
            "earthquake worm"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODhkNDhmNzktODFmMC00NDZiLWEzN2UtY2YwYzgzYTVlMWZmXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udeaa Locking massive sky earthquake worm back into golden doorway",
            "emotional": "\ud83c\udf05 Suzume meeting her younger self in the starlit everlasting realm"
        },
        "imdb_id": "tt16428256",
        "imdb_url": "https://www.imdb.com/title/tt16428256/",
        "plot": "Suzume, a 17-year-old girl who lives in a quiet town in Kyushu, meets a young man on a journey \"looking for doors.\" Suzume follows him to a ruin to a dilapidated building in the mountains and finds a free-standing, undisturbed door t as if \"it\" alone were saved from devastation. Suzume feels drawn by an invisible power and reaches out to the door - Soon, doors all over Japan start opening one after another. The doors that opened must be closed to shut out calamity that lies on the other side. -Stars, sunset, and the morning sky. The places she wanders into have a sky where all hours of the day seem to blend together- Beckoned by the mysterious doors, Suzume's \"journey of closing doors\" begins.",
        "actors": "Nanoka Hara, Hokuto Matsumura, Eri Fukatsu",
        "runtime": "122 min",
        "rated": "PG",
        "awards": "4 wins & 29 nominations total",
        "metascore": "77",
        "imdb_votes": "60,977",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "5pTcio2hTSw",
        "clip_url": "https://www.youtube-nocookie.com/embed/5pTcio2hTSw",
        "clip_title": "Suzume Trailer #1 (2023)",
        "clip_duration": "2:28",
        "sound_theme": "Haunting Female Vocal Chant & Cinematic Strings"
    },
    {
        "id": "m_62",
        "title": "Get Out",
        "year": 2017,
        "genres": [
            "Horror",
            "Mystery",
            "Thriller"
        ],
        "director": "Jordan Peele",
        "rating": 7.8,
        "match_keywords": [
            "sunken place",
            "teacup",
            "hypnosis",
            "flash"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjUxMDQwNjcyNl5BMl5BanBnXkFtZTgwNzcwMzc0MTI@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf75 Falling endlessly into the dark cosmic Sunken Place",
            "emotional": "\ud83d\udcf7 Camera flash snapping guest out of hypnotic trance"
        },
        "imdb_id": "tt5052448",
        "imdb_url": "https://www.imdb.com/title/tt5052448/",
        "plot": "Chris and his girlfriend Rose go upstate to visit her parents for the weekend. At first, Chris reads the family's overly accommodating behavior as nervous attempts to deal with their daughter's interracial relationship, but as the weekend progresses, a series of increasingly disturbing discoveries lead him to a truth that he never could have imagined.",
        "actors": "Daniel Kaluuya, Allison Williams, Bradley Whitford",
        "runtime": "104 min",
        "rated": "R",
        "awards": "Won 1 Oscar. 154 wins & 214 nominations total",
        "metascore": "85",
        "imdb_votes": "814,293",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "DzfpyUB60YY",
        "clip_url": "https://www.youtube-nocookie.com/embed/DzfpyUB60YY",
        "clip_title": "Official Trailer \u2014 Sikiliza Kwa Wahenga & Swahili Chants",
        "clip_duration": "2:29",
        "sound_theme": "Eerie Swahili Choral Chants & Suspenseful Viola"
    },
    {
        "id": "m_63",
        "title": "Hereditary",
        "year": 2018,
        "genres": [
            "Horror",
            "Drama",
            "Mystery"
        ],
        "director": "Ari Aster",
        "rating": 7.3,
        "match_keywords": [
            "paimon",
            "treehouse",
            "attic",
            "cluck"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTEyZGQwODctYWJjZi00NjFmLTg3YmEtMzlhNjljOGZhMWMyXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udd25 Flaming silhouette in dark candlelit attic summoning circle",
            "emotional": "\ud83c\udf32 Silent morning in crowned golden treehouse"
        },
        "imdb_id": "tt7784604",
        "imdb_url": "https://www.imdb.com/title/tt7784604/",
        "plot": "When Ellen, the matriarch of the Graham family, passes away, her daughter's family begins to unravel cryptic and increasingly terrifying secrets about their ancestry. The more they discover, the more they find themselves trying to outrun the sinister fate they seem to have inherited. Making his feature debut, writer-director Ari Aster unleashes a nightmare vision of a domestic breakdown that exhibits the craft and precision of a nascent auteur, transforming a familial tragedy into something ominous and deeply disquieting, and pushing the horror movie into chilling new terrain with its shattering portrait of heritage gone to hell.",
        "actors": "Toni Collette, Milly Shapiro, Gabriel Byrne",
        "runtime": "127 min",
        "rated": "R",
        "awards": "52 wins & 112 nominations total",
        "metascore": "87",
        "imdb_votes": "453,527",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "V6wWKNij_1M",
        "clip_url": "https://www.youtube-nocookie.com/embed/V6wWKNij_1M",
        "clip_title": "Official Trailer \u2014 Colin Stetson Reborn Horns & Tongue Click",
        "clip_duration": "2:19",
        "sound_theme": "Unsettling Bass Saxophone Drones & Tragic Strings"
    },
    {
        "id": "m_64",
        "title": "The Silence of the Lambs",
        "year": 1991,
        "genres": [
            "Crime",
            "Drama",
            "Thriller"
        ],
        "director": "Jonathan Demme",
        "rating": 8.6,
        "match_keywords": [
            "hannibal lecter",
            "clarice",
            "moth",
            "fbi"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNDdhOGJhYzctYzYwZC00YmI2LWI0MjctYjg4ODdlMDExYjBlXkEyXkFqcGc@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udea8 Night vision stalk in pitch black basement labyrinth",
            "emotional": "\ud83e\ude9f Quid pro quo whisper through glass prison cell"
        },
        "imdb_id": "tt0102926",
        "imdb_url": "https://www.imdb.com/title/tt0102926/",
        "plot": "F.B.I. trainee Clarice Starling (Jodie Foster) works hard to advance her career, while trying to hide or put behind her West Virginia roots, of which if some knew, would automatically classify her as being backward or white trash. After graduation, she aspires to work in the agency's Behavioral Science Unit under the leadership of Jack Crawford (Scott Glenn). While she is still a trainee, Crawford asks her to question Dr. Hannibal Lecter (Sir Anthony Hopkins), a psychiatrist imprisoned, thus far, for eight years in maximum security isolation for being a serial killer who cannibalized his victims. Clarice is able to figure out the assignment is to pick Lecter's brains to help them solve another serial murder case, that of someone coined by the media as \"Buffalo Bill\" (Ted Levine), who has so far killed five victims, all located in the eastern U.S., all young women, who are slightly overweight (especially around the hips), all who were drowned in natural bodies of water, and all who were stripped of large swaths of skin. She also figures that Crawford chose her, as a woman, to be able to trigger some emotional response from Lecter. After speaking to Lecter for the first time, she realizes that everything with him will be a psychological game, with her often having to read between the very cryptic lines he provides. She has to decide how much she will play along, as his request in return for talking to him is to expose herself emotionally to him. The case takes a more dire turn when a sixth victim is discovered, this one from who they are able to retrieve a key piece of evidence, if Lecter is being forthright as to its meaning. A potential seventh victim is high profile Catherine Martin (Brooke Smith), the daughter of Senator Ruth Martin (Diane Baker), which places greater scrutiny on the case as they search for a hopefully still alive Catherine. Who may factor into what happens is Dr. Frederick Chilton (Anthony Heald), the warden at the prison, an opportunist who sees the higher profile with Catherine, meaning a higher profile for himself if he can insert himself successfully into the proceedings.",
        "actors": "Jodie Foster, Anthony Hopkins, Scott Glenn",
        "runtime": "118 min",
        "rated": "R",
        "awards": "Won 5 Oscars. 71 wins & 50 nominations total",
        "metascore": "86",
        "imdb_votes": "1,718,588",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "W6Mm8Sbe__o",
        "clip_url": "https://www.youtube-nocookie.com/embed/W6Mm8Sbe__o",
        "clip_title": "Official Trailer \u2014 Howard Shore Clarinet & Chianti Slurp",
        "clip_duration": "2:14",
        "sound_theme": "Foreboding Low Woodwinds & Chilling Orchestral Chords"
    },
    {
        "id": "m_65",
        "title": "The Shining",
        "year": 1980,
        "genres": [
            "Horror",
            "Drama"
        ],
        "director": "Stanley Kubrick",
        "rating": 8.4,
        "match_keywords": [
            "overlook hotel",
            "redrum",
            "maze",
            "axe"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNmM5ZThhY2ItOGRjOS00NzZiLWEwYTItNDgyMjFkOTgxMmRiXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83e\ude93 Here's Johnny axe chopping through bathroom door",
            "emotional": "\u2744\ufe0f Frozen portrait in the 1921 July 4th Overlook ballroom photo"
        },
        "imdb_id": "tt0081505",
        "imdb_url": "https://www.imdb.com/title/tt0081505/",
        "plot": "Haunted by a persistent writer's block, the aspiring author and recovering alcoholic, Jack Torrance, drags his wife, Wendy, and his gifted son, Danny, up snow-capped Colorado's secluded Overlook Hotel after taking up a job as an off-season caretaker. As the cavernous hotel shuts down for the season, the manager gives Jack a grand tour, and the facility's chef, the ageing Mr Hallorann, has a fascinating chat with Danny about a rare psychic gift called \"The Shining\", making sure to warn him about the hotel's abandoned rooms, and, in particular, the off-limits Room 237. However, instead of overcoming the dismal creative rut, little by little, Jack starts losing his mind, trapped in an unforgiving environment of seemingly endless snowstorms, and a gargantuan silent prison riddled with strange occurrences and eerie visions. Now, the incessant voices inside Jack's head demand sacrifice. Is Jack capable of murder?",
        "actors": "Jack Nicholson, Shelley Duvall, Danny Lloyd",
        "runtime": "146 min",
        "rated": "R",
        "awards": "6 wins & 9 nominations total",
        "metascore": "68",
        "imdb_votes": "1,216,349",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "S014oGZiSdI",
        "clip_url": "https://www.youtube-nocookie.com/embed/S014oGZiSdI",
        "clip_title": "Official Trailer \u2014 Dies Irae & Wendy Carlos Moog Synth",
        "clip_duration": "2:17",
        "sound_theme": "Deep Analog Moog Synthesizer & Penderecki Shrieking Strings"
    },
    {
        "id": "m_80",
        "title": "A Quiet Place",
        "year": 2018,
        "genres": [
            "Horror",
            "Drama",
            "Sci-Fi"
        ],
        "director": "John Krasinski",
        "rating": 7.5,
        "match_keywords": [
            "silence",
            "sound creature",
            "sand path",
            "monopoly"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjI0MDMzNTQ0M15BMl5BanBnXkFtZTgwMTM5NzM3NDM@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udd0a Microphone feedback screech blasting invading blind creatures",
            "emotional": "\ud83e\udd1f Sign language from father across field: I have always loved you"
        },
        "imdb_id": "tt6644200",
        "imdb_url": "https://www.imdb.com/title/tt6644200/",
        "plot": "In a devastated Earth overrun by invincible predators of a possible extraterrestrial origin, the Abbotts find themselves struggling to survive in the isolation of upstate New York, defined by a new era of utter silence. Indeed, as this new type of invader is attracted to noise, even the slightest of sounds can be deadly; however, it's been already twelve months since the powerful monsters' first sightings, and this resilient family still stands strong. Of course, learning the rules of survival in this muted dystopia is essential; nevertheless, now, of all times, an otherwise joyous event puts in jeopardy the already fragile stability. And now, more than ever, the Abbotts must not make a sound.",
        "actors": "Emily Blunt, John Krasinski, Millicent Simmonds",
        "runtime": "90 min",
        "rated": "PG-13",
        "awards": "Nominated for 1 Oscar. 38 wins & 129 nominations total",
        "metascore": "82",
        "imdb_votes": "652,123",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "WR7cc5t7tv8",
        "clip_url": "https://www.youtube-nocookie.com/embed/WR7cc5t7tv8",
        "clip_title": "Official Trailer \u2014 Absolute Silence & Heartbeat Percussion",
        "clip_duration": "2:20",
        "sound_theme": "Ultra-Quiet Ambient Whispers & Sudden Sub-Drop Impact"
    },
    {
        "id": "m_81",
        "title": "Midsommar",
        "year": 2019,
        "genres": [
            "Horror",
            "Drama",
            "Mystery"
        ],
        "director": "Ari Aster",
        "rating": 7.1,
        "match_keywords": [
            "sweden",
            "maypole",
            "attestupa",
            "flower crown"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzQxNzQzOTQwM15BMl5BanBnXkFtZTgwMDQ2NTcwODM@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf38 Maypole frenetic folk dance in 24-hour sunlit Swedish meadow",
            "emotional": "\ud83d\udc51 Dani smiling under massive vibrant yellow May Queen flower gown"
        },
        "imdb_id": "tt8772262",
        "imdb_url": "https://www.imdb.com/title/tt8772262/",
        "plot": "Dani (Florence Pugh) and Christian (Jack Reynor) are a young American couple with a relationship on the brink of falling apart. But after a family tragedy keeps them together, Christian invites a grieving Dani to join him and his friends on a trip to a once-in-a-lifetime midsummer festival in a remote Swedish village. What begins as a carefree summer holiday in the North European land of eternal sunlight takes a sinister turn when the insular villagers invite their guests to partake in festivities that render the pastoral paradise increasingly unnerving and viscerally disturbing.",
        "actors": "Florence Pugh, Jack Reynor, Vilhelm Blomgren",
        "runtime": "148 min",
        "rated": "R",
        "awards": "27 wins & 74 nominations total",
        "metascore": "72",
        "imdb_votes": "481,955",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "1Vnghdsjmd0",
        "clip_url": "https://www.youtube-nocookie.com/embed/1Vnghdsjmd0",
        "clip_title": "Official Trailer \u2014 Haxan Cloak Nordic Folk & Flute Chimes",
        "clip_duration": "2:26",
        "sound_theme": "Disturbing Sunlit Pagan Folk Chants & Hurdy-Gurdy"
    },
    {
        "id": "m_82",
        "title": "Gone Girl",
        "year": 2014,
        "genres": [
            "Drama",
            "Mystery",
            "Thriller"
        ],
        "director": "David Fincher",
        "rating": 8.1,
        "match_keywords": [
            "cool girl",
            "amy dunne",
            "diary",
            "treasure hunt"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTk0MDQ3MzAzOV5BMl5BanBnXkFtZTgwNzU1NzE3MjE@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83e\ude78 Amy Dunne returning home in bloodsoaked white silk dress",
            "emotional": "\ud83d\udcd6 The Cool Girl monologue over New York brownstone memories"
        },
        "imdb_id": "tt2267998",
        "imdb_url": "https://www.imdb.com/title/tt2267998/",
        "plot": "On the occasion of his fifth wedding anniversary, Nick Dunne reports that his wife, Amy, has gone missing. Under pressure from the police and a growing media frenzy, Nick's portrait of a blissful union begins to crumble. Soon his lies, deceits and strange behavior have everyone asking the same dark question: Did Nick Dunne kill his wife?",
        "actors": "Ben Affleck, Rosamund Pike, Neil Patrick Harris",
        "runtime": "149 min",
        "rated": "R",
        "awards": "Nominated for 1 Oscar. 64 wins & 189 nominations total",
        "metascore": "79",
        "imdb_votes": "1,166,585",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "2-_-1nJf8Vg",
        "clip_url": "https://www.youtube-nocookie.com/embed/2-_-1nJf8Vg",
        "clip_title": "Official Trailer \u2014 Trent Reznor What Have We Done To Each Other",
        "clip_duration": "2:27",
        "sound_theme": "Dark Ambient Analog Synth Drone & Eerie Vocal Sample"
    },
    {
        "id": "m_83",
        "title": "Knives Out",
        "year": 2019,
        "genres": [
            "Comedy",
            "Crime",
            "Drama",
            "Mystery"
        ],
        "director": "Rian Johnson",
        "rating": 7.9,
        "match_keywords": [
            "benoit blanc",
            "mansion",
            "will",
            "donut hole"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDU5ZTRkYmItZjg0Mi00ZTQwLThjMWItNWM3MTMxMzVjZmVjXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2615 My House My Rules My Coffee mug balcony finale",
            "emotional": "\ud83c\udf69 Benoit Blanc donut hole mystery monologue in library"
        },
        "imdb_id": "tt8946378",
        "imdb_url": "https://www.imdb.com/title/tt8946378/",
        "plot": "When renowned crime novelist Harlan Thrombey (Christopher Plummer) is found dead at his estate just after his 85th birthday, the inquisitive and debonair Detective Benoit Blanc (Daniel Craig) is mysteriously enlisted to investigate. From Harlan's disfunctional family to his devoted staff, Blanc sifts through a web of red herrings and self-serving lies to uncover the truth behind Harlan's untimely death.",
        "actors": "Daniel Craig, Chris Evans, Ana de Armas",
        "runtime": "130 min",
        "rated": "PG-13",
        "awards": "Nominated for 1 Oscar. 52 wins & 114 nominations total",
        "metascore": "82",
        "imdb_votes": "875,016",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "qGqiHJTsRkQ",
        "clip_url": "https://www.youtube-nocookie.com/embed/qGqiHJTsRkQ",
        "clip_title": "Knives Out (2019 Movie) Official Trailer",
        "clip_duration": "2:23",
        "sound_theme": "Playful Whodunit Staccato Violins & Harpsichord Plucks"
    },
    {
        "id": "m_84",
        "title": "Prisoners",
        "year": 2013,
        "genres": [
            "Crime",
            "Drama",
            "Mystery",
            "Thriller"
        ],
        "director": "Denis Villeneuve",
        "rating": 8.2,
        "match_keywords": [
            "hugh jackman",
            "maze",
            "detective loki",
            "whistle"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTg0NTIzMjQ1NV5BMl5BanBnXkFtZTcwNDc3MzM5OQ@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\ude97 Detective Loki high-speed rainy night hospital run with bleeding eyes",
            "emotional": "\ud83d\udea8 Faint whistle sound heard from beneath the frozen yard pit"
        },
        "imdb_id": "tt1392214",
        "imdb_url": "https://www.imdb.com/title/tt1392214/",
        "plot": "How far would you go to protect your family? Keller Dover is facing every parent's worst nightmare. His six-year-old daughter, Anna, is missing, together with her young friend, Joy, and as minutes turn to hours, panic sets in. The only lead is a dilapidated RV that had earlier been parked on their street. Heading the investigation, Detective Loki arrests its driver, Alex Jones, but a lack of evidence forces his release. As the police pursue multiple leads and pressure mounts, knowing his child's life is at stake the frantic Dover decides he has no choice but to take matters into his own hands. But just how far will this desperate father go to protect his family?",
        "actors": "Hugh Jackman, Jake Gyllenhaal, Viola Davis",
        "runtime": "153 min",
        "rated": "R",
        "awards": "Nominated for 1 Oscar. 10 wins & 38 nominations total",
        "metascore": "70",
        "imdb_votes": "922,474",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "bpXfcTF6iVk",
        "clip_url": "https://www.youtube-nocookie.com/embed/bpXfcTF6iVk",
        "clip_title": "Official Trailer \u2014 J\u00f3hann J\u00f3hannsson Heavy Organ & Rain",
        "clip_duration": "2:28",
        "sound_theme": "Dismal Icelandic Cello & Church Organ Drone"
    },
    {
        "id": "m_85",
        "title": "Memento",
        "year": 2000,
        "genres": [
            "Mystery",
            "Thriller"
        ],
        "director": "Christopher Nolan",
        "rating": 8.4,
        "match_keywords": [
            "polaroid",
            "tattoos",
            "short term memory",
            "sammy jankis"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMGQ3Y2Q4NjktN2E4Ny00Y2Q2LTliZDUtZTNiNjRhY2I0NGIyXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udcf8 Reverse polaroid developing backward into blank image",
            "emotional": "\ud83d\udcdd Writing Don't believe his lies on the back of photo"
        },
        "imdb_id": "tt0209144",
        "imdb_url": "https://www.imdb.com/title/tt0209144/",
        "plot": "Memento chronicles two separate stories of Leonard, an ex-insurance investigator who can no longer build new memories, as he attempts to find the murderer of his wife, which is the last thing he remembers. One story line moves forward in time while the other tells the story backwards revealing more each time.",
        "actors": "Guy Pearce, Carrie-Anne Moss, Joe Pantoliano",
        "runtime": "113 min",
        "rated": "R",
        "awards": "Nominated for 2 Oscars. 57 wins & 59 nominations total",
        "metascore": "83",
        "imdb_votes": "1,432,382",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "4CV41hoyS8A",
        "clip_url": "https://www.youtube-nocookie.com/embed/4CV41hoyS8A",
        "clip_title": "Official Trailer \u2014 David Julyan Reverse Ambient Soundscape",
        "clip_duration": "2:14",
        "sound_theme": "Subtle Reversing Ambient Piano & Ticking Polaroid"
    },
    {
        "id": "m_86",
        "title": "The Grand Budapest Hotel",
        "year": 2014,
        "genres": [
            "Adventure",
            "Comedy",
            "Crime"
        ],
        "director": "Wes Anderson",
        "rating": 8.1,
        "match_keywords": [
            "gustave h",
            "zero",
            "courtesan au chocolat",
            "boy with apple"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMzM5NjUxOTEyMl5BMl5BanBnXkFtZTgwNjEyMDM0MDE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfbf Downhill luge & bobsled chase through snowy Alpine peaks",
            "emotional": "\ud83c\udf70 Unboxing pastel pink Mendl's Courtesan au Chocolat pastries"
        },
        "imdb_id": "tt2278388",
        "imdb_url": "https://www.imdb.com/title/tt2278388/",
        "plot": "This movie recounts the adventures of M. Gustave, a legendary concierge at a famous European hotel between the wars, and Zero Moustafa, the lobby boy who becomes his most trusted friend. The story involves the theft and recovery of a priceless Renaissance painting and the battle for an enormous family fortune - all against the backdrop of a suddenly and dramatically changing continent.",
        "actors": "Ralph Fiennes, F. Murray Abraham, Mathieu Amalric",
        "runtime": "99 min",
        "rated": "R",
        "awards": "Won 4 Oscars. 137 wins & 227 nominations total",
        "metascore": "88",
        "imdb_votes": "968,286",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "1Fg5iWmQjwk",
        "clip_url": "https://www.youtube-nocookie.com/embed/1Fg5iWmQjwk",
        "clip_title": "Official Trailer \u2014 Alexandre Desplat Balalaika & Cimbalom",
        "clip_duration": "2:24",
        "sound_theme": "Fast East-European Balalaika & Whimsical Cimbalom"
    },
    {
        "id": "m_87",
        "title": "Everything Everywhere All at Once",
        "year": 2022,
        "genres": [
            "Action",
            "Adventure",
            "Comedy",
            "Sci-Fi"
        ],
        "director": "Daniel Kwan & Daniel Scheinert",
        "rating": 7.8,
        "match_keywords": [
            "multiverse",
            "bagel",
            "hot dog fingers",
            "googly eyes"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOWNmMzAzZmQtNDQ1NC00Nzk5LTkyMmUtNGI2N2NkOWM4MzEyXkEyXkFqcGc@._V1_QL75_UY562_CR4,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83e\udd4b Fanny pack kung fu battle through IRS tax office corridors",
            "emotional": "\ud83e\udea8 Two silent rocks overlooking grand canyon with text dialogues"
        },
        "imdb_id": "tt6710474",
        "imdb_url": "https://www.imdb.com/title/tt6710474/",
        "plot": "With her laundromat teetering on the brink of failure and her marriage to wimpy husband Waymond on the rocks, overworked Evelyn Wang struggles to cope with everything, including a tattered relationship with her judgmental father and daughter. And as if facing a gloomy midlife crisis wasn't enough, Evelyn must brace herself up for an unpleasant meeting with an impersonal bureaucrat: Deirdre, the shabbily dressed IRS auditor. However, as the stern agent loses patience, an inexplicable multiverse rift becomes an eye-opening exploration of parallel realities. Will Evelyn jump down the rabbit hole? But how many stars are in the universe? Can weary Evelyn fathom the irrepressible force of possibilities, tap into newfound powers, and prevent an evil entity from destroying the thin, countless layers of the unseen world?",
        "actors": "Michelle Yeoh, Stephanie Hsu, Jamie Lee Curtis",
        "runtime": "139 min",
        "rated": "R",
        "awards": "Won 7 Oscars. 408 wins & 382 nominations total",
        "metascore": "81",
        "imdb_votes": "627,115",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "wxN1T1uxQ2g",
        "clip_url": "https://www.youtube-nocookie.com/embed/wxN1T1uxQ2g",
        "clip_title": "Official Trailer \u2014 Son Lux This Is A Life & Googly Eye Beat",
        "clip_duration": "2:44",
        "sound_theme": "Multiverse Glitch Electronic Beats & Emotional Choirs"
    },
    {
        "id": "m_88",
        "title": "Superbad",
        "year": 2007,
        "genres": [
            "Comedy"
        ],
        "director": "Greg Mottola",
        "rating": 7.6,
        "match_keywords": [
            "mclovin",
            "fake id",
            "party",
            "police cruiser"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNjk0MzdlZGEtNTRkOC00ZDRiLWJkYjAtMzUzYTRiNzk1YTViXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\ude94 Police cruiser donut spin in convenience store parking lot",
            "emotional": "\ud83d\uded2 Seth and Evan hugging goodbye on mall escalator"
        },
        "imdb_id": "tt0829482",
        "imdb_url": "https://www.imdb.com/title/tt0829482/",
        "plot": "Seth and Evan are best friends, inseparable, navigating the last weeks of high school. Usually shunned by the popular kids, Seth and Evan luck into an invitation to a party, and spend a long day, with the help of their nerdy friend Fogell, trying to score enough alcohol to lubricate the party and inebriate two girls, Jules and Becca, so they can kick-start their sex lives and go off to college with a summer full of experience and new skills. Their quest is complicated by Fogell's falling in with two inept cops who both slow and assist the plan. If they do get the liquor to the party, what then? Is sex the only rite of passage at hand?",
        "actors": "Michael Cera, Jonah Hill, Christopher Mintz-Plasse",
        "runtime": "113 min",
        "rated": "R",
        "awards": "11 wins & 24 nominations total",
        "metascore": "76",
        "imdb_votes": "687,483",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "4eaZ_48ZYog",
        "clip_url": "https://www.youtube-nocookie.com/embed/4eaZ_48ZYog",
        "clip_title": "Official Trailer \u2014 Superbad Funk & McLovin Brass",
        "clip_duration": "2:26",
        "sound_theme": "70s Blaxploitation Wah-Wah Guitar & Tight Funk Bass"
    },
    {
        "id": "m_89",
        "title": "The Big Lebowski",
        "year": 1998,
        "genres": [
            "Comedy",
            "Crime"
        ],
        "director": "Joel & Ethan Coen",
        "rating": 8.1,
        "match_keywords": [
            "the dude",
            "rug",
            "bowling",
            "white russian"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BY2E3OWQ5OWYtYTRkMC00NjVjLWIzZDQtNmRmM2ZiYTIyYmYxXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udfb3 Surreal dream sequence flying down bowling alley lane",
            "emotional": "\ud83e\udd43 The Dude sipping White Russian: The Dude abides"
        },
        "imdb_id": "tt0118715",
        "imdb_url": "https://www.imdb.com/title/tt0118715/",
        "plot": "When \"the dude\" Lebowski is mistaken for a millionaire Lebowski, two thugs urinate on his rug to coerce him into paying a debt he knows nothing about. While attempting to gain recompense for the ruined rug from his wealthy counterpart, he accepts a one-time job with high pay-off. He enlists the help of his bowling buddy, Walter, a gun-toting Jewish-convert with anger issues. Deception leads to more trouble, and it soon seems that everyone from porn empire tycoons to nihilists want something from The Dude.",
        "actors": "Jeff Bridges, John Goodman, Julianne Moore",
        "runtime": "117 min",
        "rated": "R",
        "awards": "7 wins & 18 nominations total",
        "metascore": "71",
        "imdb_votes": "911,908",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "cd-go0oBF4Y",
        "clip_url": "https://www.youtube-nocookie.com/embed/cd-go0oBF4Y",
        "clip_title": "Official Trailer \u2014 The Man in Me by Bob Dylan & Bowling Strike",
        "clip_duration": "2:28",
        "sound_theme": "Laid-back 70s Acoustic Folk & Crashing Bowling Pins"
    },
    {
        "id": "m_90",
        "title": "Deadpool",
        "year": 2016,
        "genres": [
            "Action",
            "Comedy",
            "Sci-Fi"
        ],
        "director": "Tim Miller",
        "rating": 8.0,
        "match_keywords": [
            "fourth wall",
            "chimichanga",
            "wadewilson",
            "kurt cobain"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzY3ZWU5NGQtOTViNC00ZWVmLTliNjAtNzViNzlkZWQ4YzQ4XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\u2694\ufe0f Highway overpass bullet countdown acrobatics",
            "emotional": "\u2764\ufe0f Careless Whisper boombox serenade in warehouse"
        },
        "imdb_id": "tt1431045",
        "imdb_url": "https://www.imdb.com/title/tt1431045/",
        "plot": "This is the origin story of former Special Forces operative turned mercenary Wade Wilson, who after being subjected to a rogue experiment that leaves him with accelerated healing powers, adopts the alter ego Deadpool. Armed with his new abilities and a dark, twisted sense of humor, Deadpool hunts down the man who nearly destroyed his life.",
        "actors": "Ryan Reynolds, Morena Baccarin, T.J. Miller",
        "runtime": "108 min",
        "rated": "R",
        "awards": "29 wins & 78 nominations total",
        "metascore": "65",
        "imdb_votes": "1,250,978",
        "media_type": "movie",
        "total_seasons": "Feature Film",
        "trailer_id": "ONHBaC-pfsk",
        "clip_url": "https://www.youtube-nocookie.com/embed/ONHBaC-pfsk",
        "clip_title": "Official Red Band Trailer \u2014 Shoop by Salt-N-Pepa & Wham!",
        "clip_duration": "2:56",
        "sound_theme": "90s Hip-Hop Groove & Hard Rock Guitar Riffs"
    },
    {
        "id": "s_01",
        "title": "Peaky Blinders",
        "year": "2013\u20132022",
        "media_type": "series",
        "total_seasons": "6 Seasons",
        "genres": [
            "Crime",
            "Drama"
        ],
        "director": "Created by Steven Knight",
        "rating": 8.7,
        "match_keywords": [
            "peaky blinders",
            "tommy shelby",
            "birmingham",
            "gangster",
            "razor"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOGM0NGY3ZmItOGE2ZC00OWIxLTk0N2EtZWY4Yzg3ZDlhNGI3XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83e\udd43 Thomas Shelby walking through Birmingham sparks in flat cap",
            "emotional": "\ud83d\udeac Tommy Shelby looking over mist hills: By order of the Peaky Blinders"
        },
        "imdb_id": "tt2442560",
        "imdb_url": "https://www.imdb.com/title/tt2442560/",
        "plot": "Thomas Shelby and his brothers return to Birmingham after serving in the British Army during WWI. Shelby and his gang, the Peaky Blinders, control the city of Birmingham. However, Shelby's ambitions extend beyond Birmingham, as he plans to build on the business empire he's created, and dispatch anyone who gets in his way.",
        "actors": "Cillian Murphy, Paul Anderson, Sophie Rundle",
        "runtime": "6 Seasons \u2022 60 min",
        "rated": "TV-MA",
        "awards": "Won 1 BAFTA Award. 25 wins & 56 nominations total",
        "metascore": "88",
        "imdb_votes": "771,795",
        "trailer_id": "oVzVdvGIC7U",
        "clip_url": "https://www.youtube-nocookie.com/embed/oVzVdvGIC7U",
        "clip_title": "Series Trailer \u2014 Red Right Hand by Nick Cave & Gunfire",
        "clip_duration": "2:15",
        "sound_theme": "Nick Cave Dark Blues Rock & Birmingham Bell Tolls"
    },
    {
        "id": "s_02",
        "title": "Money Heist",
        "year": "2017\u20132021",
        "media_type": "series",
        "total_seasons": "5 Seasons",
        "genres": [
            "Action",
            "Crime",
            "Drama"
        ],
        "director": "Created by \u00c1lex Pina",
        "rating": 8.2,
        "match_keywords": [
            "professor",
            "royal mint",
            "dali mask",
            "heist",
            "tokyo"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjkxZWJiNTUtYjQwYS00MTBlLTgwODQtM2FkNWMyMjMwOGZiXkEyXkFqcGc@._V1_QL75_UX380_CR0,5,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfad Dali mask crew holding red jumpsuits in Royal Mint vault",
            "emotional": "\ud83c\udfb5 Bella Ciao singing duet at the rustic hideout piano"
        },
        "imdb_id": "tt6468322",
        "imdb_url": "https://www.imdb.com/title/tt6468322/",
        "plot": "To carry out the biggest heist in history, a mysterious man called The Professor recruits a band of eight robbers who have a single characteristic: none of them has anything to lose. Five months of seclusion memorizing every step, every detail, every probability culminate in eleven days locked up in the National Coinage and Stamp Factory of Spain, surrounded by police forces and with dozens of hostages in their power, to find out whether their suicide wager will lead to everything or nothing.",
        "actors": "\u00darsula Corber\u00f3, \u00c1lvaro Morte, Itziar Itu\u00f1o",
        "runtime": "5 Seasons \u2022 70 min",
        "rated": "TV-MA",
        "awards": "37 wins & 47 nominations total",
        "metascore": "88",
        "imdb_votes": "604,616",
        "trailer_id": "_InqQJRqGW4",
        "clip_url": "https://www.youtube-nocookie.com/embed/_InqQJRqGW4",
        "clip_title": "Series Trailer \u2014 Bella Ciao & Spanish Royal Mint Alarm",
        "clip_duration": "2:07",
        "sound_theme": "Chant of Bella Ciao & Pulsing Electronic Heist Bass"
    },
    {
        "id": "s_03",
        "title": "The Mentalist",
        "year": "2008\u20132015",
        "media_type": "series",
        "total_seasons": "7 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Mystery"
        ],
        "director": "Created by Bruno Heller",
        "rating": 8.2,
        "match_keywords": [
            "patrick jane",
            "cbi",
            "red john",
            "psychic",
            "deduction"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ5OTgzOTczM15BMl5BanBnXkFtZTcwMDM2OTY4MQ@@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\u2615 Patrick Jane smiling calmly solving murder in interrogation room",
            "emotional": "\ud83d\udd34 Red John smiley face painted on wall in dark bedroom"
        },
        "imdb_id": "tt1196946",
        "imdb_url": "https://www.imdb.com/title/tt1196946/",
        "plot": "Patrick Jane is a crime consultant with the California Bureau of Investigation. He has a particular gift for astute observation and reading people, honed through years of being a faux psychic. His gift makes him brilliant at solving murders, which is why the CBI have him around. However, his motive for taking on the role is purely one of revenge: find and kill the man who killed his wife and daughter - Red John.",
        "actors": "Simon Baker, Robin Tunney, Tim Kang",
        "runtime": "7 Seasons \u2022 43 min",
        "rated": "TV-14",
        "awards": "Nominated for 1 Primetime Emmy. 4 wins & 16 nominations total",
        "metascore": "88",
        "imdb_votes": "221,480",
        "trailer_id": "nn2Q69pSC_M",
        "clip_url": "https://www.youtube-nocookie.com/embed/nn2Q69pSC_M",
        "clip_title": "The Mentalist  trailer",
        "clip_duration": "2:02",
        "sound_theme": "Clever Whimsical Piano & Acoustic Mystery Melody"
    },
    {
        "id": "s_04",
        "title": "Breaking Bad",
        "year": "2008\u20132013",
        "media_type": "series",
        "total_seasons": "5 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Thriller"
        ],
        "director": "Created by Vince Gilligan",
        "rating": 9.5,
        "match_keywords": [
            "walter white",
            "heisenberg",
            "jesse pinkman",
            "meth",
            "albuquerque"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOWE4NTc3YmYtNmU2Mi00ZjhkLWE1MTItZmM1M2U1ODU3YjFlXkEyXkFqcGc@._V1_QL75_UY562_CR2,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2697\ufe0f Walter White in yellow hazmat suit adjusting RV lab burner",
            "emotional": "\ud83c\udfa9 Say my name: You're Heisenberg. You're goddamn right."
        },
        "imdb_id": "tt0903747",
        "imdb_url": "https://www.imdb.com/title/tt0903747/",
        "plot": "Walter White is a chemistry genius but works as a chemistry teacher at a high school in Albuquerque, New Mexico. His life drastically changes when he's diagnosed with stage III terminal lung cancer and given a prognosis of two years to live. To ensure that his pregnant wife and disabled teenage son have a financial future, he uses his chemistry background to create and sell the world's finest crystal methamphetamine. To sell his signature \"blue meth,\" he teams up with Jesse Pinkman, a former student of his. The meth makes them very rich very quickly, but it attracts the attention of his DEA brother-in-law, Hank. As Walter and Jesse's status in the drug world escalates, Walter becomes a dangerous criminal, and Jesse becomes a hot-headed salesman. Hank is always hot on his tail, forcing Walter to devise new ways to cover his tracks.",
        "actors": "Bryan Cranston, Aaron Paul, Anna Gunn",
        "runtime": "5 Seasons \u2022 49 min",
        "rated": "TV-MA",
        "awards": "Won 16 Primetime Emmys. 172 wins & 269 nominations total",
        "metascore": "88",
        "imdb_votes": "2,671,962",
        "trailer_id": "HhesaQXLuRY",
        "clip_url": "https://www.youtube-nocookie.com/embed/HhesaQXLuRY",
        "clip_title": "Series Trailer \u2014 Dave Porter Desert Dobro & Heisenberg Riser",
        "clip_duration": "2:20",
        "sound_theme": "Gritty Resonator Guitar & Chemical Laboratory Drone"
    },
    {
        "id": "s_05",
        "title": "Better Call Saul",
        "year": "2015\u20132022",
        "media_type": "series",
        "total_seasons": "6 Seasons",
        "genres": [
            "Crime",
            "Drama"
        ],
        "director": "Created by Vince Gilligan & Peter Gould",
        "rating": 9.0,
        "match_keywords": [
            "jimmy mcgill",
            "saul goodman",
            "kim wexler",
            "lawyer",
            "gus fring"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTAxOTQ0MjUzMzJeQTJeQWpwZ15BbWU4MDY0NTAxNzMx._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2696\ufe0f Jimmy McGill arguing passionate court defense in Albuquerque",
            "emotional": "\ud83d\udeac Jimmy and Kim sharing cigarette leaning against brick wall"
        },
        "imdb_id": "tt3032476",
        "imdb_url": "https://www.imdb.com/title/tt3032476/",
        "plot": "Before Saul Goodman, he was Jimmy McGill. And if you're calling Jimmy, you're in real trouble. The prequel to \"Breaking Bad\" follows small-time attorney, Jimmy McGill, as he transforms into Walter White's morally challenged lawyer, Saul Goodman.",
        "actors": "Bob Odenkirk, Rhea Seehorn, Jonathan Banks",
        "runtime": "6 Seasons \u2022 46 min",
        "rated": "TV-MA",
        "awards": "Nominated for 53 Primetime Emmys. 66 wins & 317 nominations total",
        "metascore": "88",
        "imdb_votes": "862,017",
        "trailer_id": "HN4oydykJFc",
        "clip_url": "https://www.youtube-nocookie.com/embed/HN4oydykJFc",
        "clip_title": "Better Call Saul | Series Trailer",
        "clip_duration": "2:14",
        "sound_theme": "Punchy Garage Rock Blues Guitar & Snappy Drums"
    },
    {
        "id": "s_06",
        "title": "Game of Thrones",
        "year": "2011\u20132019",
        "media_type": "series",
        "total_seasons": "8 Seasons",
        "genres": [
            "Action",
            "Adventure",
            "Drama",
            "Fantasy"
        ],
        "director": "Created by David Benioff & D.B. Weiss",
        "rating": 9.2,
        "match_keywords": [
            "westeros",
            "iron throne",
            "dragons",
            "winter is coming",
            "jon snow"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTNhMDJmNmYtNDQ5OS00ODdlLWE0ZDAtZTgyYTIwNDY3OTU3XkEyXkFqcGc@._V1_QL75_UX380_CR0,3,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udc09 Daenerys riding Drogon breathing fire over battle fleet",
            "emotional": "\u2744\ufe0f Jon Snow facing charging cavalry army with drawn sword"
        },
        "imdb_id": "tt0944947",
        "imdb_url": "https://www.imdb.com/title/tt0944947/",
        "plot": "In the mythical continent of Westeros, several powerful families fight for control of the Seven Kingdoms. As conflict erupts in the kingdoms of men, an ancient enemy rises once again to threaten them all. Meanwhile, the last heirs of a recently usurped dynasty plot to take back their homeland from across the Narrow Sea.",
        "actors": "Emilia Clarke, Peter Dinklage, Kit Harington",
        "runtime": "8 Seasons \u2022 57 min",
        "rated": "TV-MA",
        "awards": "Won 59 Primetime Emmys. 396 wins & 655 nominations total",
        "metascore": "88",
        "imdb_votes": "2,606,100",
        "trailer_id": "KPLWWIOCOOQ",
        "clip_url": "https://www.youtube-nocookie.com/embed/KPLWWIOCOOQ",
        "clip_title": "Series Trailer \u2014 Ramin Djawadi Theme & Dragon Roar",
        "clip_duration": "2:20",
        "sound_theme": "Iconic Cello Battle Fanfare & Massive War Drums"
    },
    {
        "id": "s_07",
        "title": "House of the Dragon",
        "year": "2022\u2013",
        "media_type": "series",
        "total_seasons": "4 Seasons",
        "genres": [
            "Action",
            "Adventure",
            "Drama",
            "Fantasy"
        ],
        "director": "Created by Ryan J. Condal & George R.R. Martin",
        "rating": 8.3,
        "match_keywords": [
            "targaryen",
            "vhagar",
            "daemon",
            "rhaenyra",
            "dragons"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZGM4MTczODQtNGIxOC00Y2U2LTk1YmItNzA2N2VhYmE0Y2YwXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udc32 Vhagar giant dragon descending through dark storm clouds",
            "emotional": "\ud83d\udc51 King Viserys slow walk to Iron Throne with gold mask"
        },
        "imdb_id": "tt11198330",
        "imdb_url": "https://www.imdb.com/title/tt11198330/",
        "plot": "The Targaryen dynasty is at the absolute apex of its power, with more than 10 dragons under their yoke. Most empires crumble from such heights. In the case of the Targaryens, their slow fall begins when King Viserys breaks with a century of tradition by naming his daughter Rhaenyra heir to the Iron Throne. But when Viserys later fathers a son, the court is shocked when Rhaenyra retains her status as his heir, and seeds of division sow friction across the realm.",
        "actors": "Matt Smith, Emma D&apos;Arcy, Olivia Cooke",
        "runtime": "4 Seasons \u2022 N/A",
        "rated": "TV-MA",
        "awards": "Won 2 Primetime Emmys. 23 wins & 99 nominations total",
        "metascore": "88",
        "imdb_votes": "543,152",
        "trailer_id": "DotnJ7tTA34",
        "clip_url": "https://www.youtube-nocookie.com/embed/DotnJ7tTA34",
        "clip_title": "Series Trailer \u2014 House Targaryen Valyrian Horns & Fire",
        "clip_duration": "2:24",
        "sound_theme": "Dark Valyrian Choral Chants & Epic Battle Orchestra"
    },
    {
        "id": "s_08",
        "title": "Stranger Things",
        "year": "2016\u20132025",
        "media_type": "series",
        "total_seasons": "5 Seasons",
        "genres": [
            "Drama",
            "Fantasy",
            "Horror",
            "Sci-Fi"
        ],
        "director": "Created by The Duffer Brothers",
        "rating": 8.6,
        "match_keywords": [
            "upside down",
            "eleven",
            "demogorgon",
            "hawkins",
            "80s"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNjRiMTA4NWUtNmE0ZC00NGM0LWJhMDUtZWIzMDM5ZDIzNTg3XkEyXkFqcGc@._V1_QL75_UY562_CR35,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udeb2 Kids riding bikes through Hawkins woods escaping Demogorgon",
            "emotional": "\ud83d\udca1 Christmas light alphabet glowing on Joyce living room wall"
        },
        "imdb_id": "tt4574334",
        "imdb_url": "https://www.imdb.com/title/tt4574334/",
        "plot": "When Will Byers suddenly goes missing, the whole town of Hawkins, Indiana, turns upside down. Many people are on the search for Will, including his mother Joyce, his brother Jonathan, his friends Mike, Dustin, and Lucas, Police Chief Jim Hopper, and other notable people. But one thing leads to another, creating a supernatural trail. And things get even weirder when a little girl with a shaved head comes into the story.",
        "actors": "Millie Bobby Brown, Finn Wolfhard, Winona Ryder",
        "runtime": "5 Seasons \u2022 51 min",
        "rated": "TV-MA",
        "awards": "Won 12 Primetime Emmys. 122 wins & 335 nominations total",
        "metascore": "88",
        "imdb_votes": "1,691,532",
        "trailer_id": "b9EkMc79ZSU",
        "clip_url": "https://www.youtube-nocookie.com/embed/b9EkMc79ZSU",
        "clip_title": "Series Trailer \u2014 S U R V I V E 80s Analog Synthesizer",
        "clip_duration": "2:40",
        "sound_theme": "Vintage Arpeggiated Moog Synth & Hawkins Bass Drone"
    },
    {
        "id": "s_09",
        "title": "Sherlock",
        "year": "2010\u20132017",
        "media_type": "series",
        "total_seasons": "4 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Mystery"
        ],
        "director": "Created by Mark Gatiss & Steven Moffat",
        "rating": 9.0,
        "match_keywords": [
            "sherlock holmes",
            "221b",
            "watson",
            "moriarty",
            "baker street"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTQzNGZjNDEtOTMwYi00MzFjLWE2ZTYtYzYxYzMwMjZkZDc5XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfbb Sherlock deducing clues with holographic floating text in 221B",
            "emotional": "\ud83c\udfe2 St. Bart's hospital rooftop jump confession to John Watson"
        },
        "imdb_id": "tt1475582",
        "imdb_url": "https://www.imdb.com/title/tt1475582/",
        "plot": "In this modernized version of the Conan Doyle characters, using his detective plots, Sherlock Holmes lives in early-21st-century London and acts more cocky towards Scotland Yard's detective inspector Lestrade because he's actually less confident. Doctor Watson is now a fairly young veteran of the Afghan war, less adoring and more active.",
        "actors": "Benedict Cumberbatch, Martin Freeman, Una Stubbs",
        "runtime": "4 Seasons \u2022 88 min",
        "rated": "TV-14",
        "awards": "Won 9 Primetime Emmys. 95 wins & 185 nominations total",
        "metascore": "88",
        "imdb_votes": "1,086,290",
        "trailer_id": "9UcR9iKArd0",
        "clip_url": "https://www.youtube-nocookie.com/embed/9UcR9iKArd0",
        "clip_title": "Series Trailer \u2014 David Arnold Baker Street Cimbalom & Violin",
        "clip_duration": "2:06",
        "sound_theme": "Fast Rapid-Fire Violin Arpeggio & Clapping Percussion"
    },
    {
        "id": "s_10",
        "title": "Dark",
        "year": "2017\u20132020",
        "media_type": "series",
        "total_seasons": "3 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Mystery",
            "Sci-Fi"
        ],
        "director": "Created by Baran bo Odar & Jantje Friese",
        "rating": 8.7,
        "match_keywords": [
            "time travel",
            "winden",
            "cave",
            "bootstrap paradox",
            "jonas"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOWJjMGViY2UtNTAzNS00ZGFjLWFkNTMtMDBiMDMyZTM1NTY3XkEyXkFqcGc@._V1_QL75_UX380_CR0,57,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf27\ufe0f Yellow raincoat Jonas walking into dark Winden cave portal",
            "emotional": "\u23f3 What we know is a drop, what we don't know is an ocean"
        },
        "imdb_id": "tt5753856",
        "imdb_url": "https://www.imdb.com/title/tt5753856/",
        "plot": "The first German production from the world's leading Internet TV Network is set in a present-day German town where the disappearance of two young children exposes the double lives and fractured relationships among four families. In 10 hour-long episodes, the story takes on a surprising twist that ties back to the same town in 1986.",
        "actors": "Louis Hofmann, Karoline Eichhorn, Lisa Vicari",
        "runtime": "3 Seasons \u2022 60 min",
        "rated": "TV-MA",
        "awards": "8 wins & 23 nominations total",
        "metascore": "88",
        "imdb_votes": "542,010",
        "trailer_id": "rrwycJ08PSA",
        "clip_url": "https://www.youtube-nocookie.com/embed/rrwycJ08PSA",
        "clip_title": "Series Trailer \u2014 Ben Frost For Everything A Time & Winden Cave",
        "clip_duration": "2:16",
        "sound_theme": "Distorted Throat Singing & Thunderous Subsonic Booms"
    },
    {
        "id": "s_11",
        "title": "Severance",
        "year": "2022\u2013",
        "media_type": "series",
        "total_seasons": "3 Seasons",
        "genres": [
            "Drama",
            "Mystery",
            "Sci-Fi",
            "Thriller"
        ],
        "director": "Created by Dan Erickson",
        "rating": 8.6,
        "match_keywords": [
            "lumon",
            "severed",
            "mark scout",
            "macrodata",
            "innies"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZDI5YzJhODQtMzQyNy00YWNmLWIxMjUtNDBjNjA5YWRjMzExXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udfe2 Walking down endless sterile white Lumon office hallways",
            "emotional": "\ud83e\uddc7 Waffle party dance in severed basement floor"
        },
        "imdb_id": "tt11280740",
        "imdb_url": "https://www.imdb.com/title/tt11280740/",
        "plot": "Mark leads a team of office workers whose memories have been surgically divided between their work and personal lives. When a mysterious colleague appears outside of work, it begins a journey to discover the truth about their jobs.",
        "actors": "Adam Scott, Britt Lower, Zach Cherry",
        "runtime": "3 Seasons \u2022 N/A",
        "rated": "TV-MA",
        "awards": "Won 10 Primetime Emmys. 51 wins & 201 nominations total",
        "metascore": "88",
        "imdb_votes": "385,489",
        "trailer_id": "xEQP4VVuyrY",
        "clip_url": "https://www.youtube-nocookie.com/embed/xEQP4VVuyrY",
        "clip_title": "Series Trailer \u2014 Theodore Shapiro Severance Theme & Elevator Chime",
        "clip_duration": "2:18",
        "sound_theme": "Eerie Repeating Piano Triplet & Retro Office Hum"
    },
    {
        "id": "s_12",
        "title": "Succession",
        "year": "2018\u20132023",
        "media_type": "series",
        "total_seasons": "4 Seasons",
        "genres": [
            "Drama"
        ],
        "director": "Created by Jesse Armstrong",
        "rating": 8.8,
        "match_keywords": [
            "logan roy",
            "waystar royco",
            "kendall roy",
            "billionaire",
            "ceo"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTY4YTVkY2QtMjRmOS00YzliLWIxOWQtMTdkOTVkN2UzODNmXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\ude81 Logan Roy boarding helicopter shouting corporate orders",
            "emotional": "\ud83c\udf0a Kendall Roy sitting alone in rooftop infinity pool"
        },
        "imdb_id": "tt7660850",
        "imdb_url": "https://www.imdb.com/title/tt7660850/",
        "plot": "The Roy family is known for controlling the biggest media and entertainment company in the world. However, their world changes when their father steps down from the company.",
        "actors": "Nicholas Braun, Brian Cox, Kieran Culkin",
        "runtime": "4 Seasons \u2022 60 min",
        "rated": "TV-MA",
        "awards": "Won 19 Primetime Emmys. 141 wins & 265 nominations total",
        "metascore": "88",
        "imdb_votes": "346,930",
        "trailer_id": "OzYxJV_rmE8",
        "clip_url": "https://www.youtube-nocookie.com/embed/OzYxJV_rmE8",
        "clip_title": "Series Trailer \u2014 Nicholas Britell Hip-Hop Piano & Strings",
        "clip_duration": "2:25",
        "sound_theme": "Heavy 808 Hip-Hop Beats with Melancholy Piano Riff"
    },
    {
        "id": "s_13",
        "title": "The Boys",
        "year": "2019\u20132026",
        "media_type": "series",
        "total_seasons": "5 Seasons",
        "genres": [
            "Action",
            "Comedy",
            "Drama",
            "Sci-Fi"
        ],
        "director": "Created by Eric Kripke",
        "rating": 8.5,
        "match_keywords": [
            "homelander",
            "billy butcher",
            "vought",
            "compound v",
            "supes"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjU4OWNiYzQtMzc1NS00NjZlLTgyYTctZWY4ZmEzMTkxYjA4XkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\u26a1 Homelander glowing red laser eyes smiling at camera",
            "emotional": "\ud83d\udee1\ufe0f Billy Butcher smirking: Oi, diabolical"
        },
        "imdb_id": "tt1190634",
        "imdb_url": "https://www.imdb.com/title/tt1190634/",
        "plot": "In The Boys, a world exists where superheroes, known as Supes, are revered as celebrities, managed by the powerful Vought International. However, beneath the glamorous facade lies a dark truth: most Supes are corrupt and abuse their powers. The story follows two groups: The Boys, vigilantes seeking revenge against Supes for past traumas, and The Seven, Vought's premiere superhero team led by the ruthless Homelander. As Hughie joins The Boys for revenge after a Supe kills his girlfriend, and the idealistic Starlight joins The Seven only to discover their corruption, both groups clash in a brutal fight to expose Vought's secrets and dismantle their control over the corrupt Supes, blurring the lines between good and evil in a world where immense power breeds immense corruption.",
        "actors": "Karl Urban, Jack Quaid, Antony Starr",
        "runtime": "5 Seasons \u2022 60 min",
        "rated": "TV-MA",
        "awards": "Won 4 Primetime Emmys. 26 wins & 100 nominations total",
        "metascore": "88",
        "imdb_votes": "1,004,801",
        "trailer_id": "M1bhOaLV4FU",
        "clip_url": "https://www.youtube-nocookie.com/embed/M1bhOaLV4FU",
        "clip_title": "The Boys - Official Trailer",
        "clip_duration": "2:31",
        "sound_theme": "Distorted Punk Rock Guitar Riffs & Crashing Cymbals"
    },
    {
        "id": "s_14",
        "title": "Fleabag",
        "year": "2016\u20132019",
        "media_type": "series",
        "total_seasons": "2 Seasons",
        "genres": [
            "Comedy",
            "Drama"
        ],
        "director": "Created by Phoebe Waller-Bridge",
        "rating": 8.7,
        "match_keywords": [
            "fourth wall",
            "hot priest",
            "guinea pig",
            "london",
            "confession"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA4MzU5NzQxNV5BMl5BanBnXkFtZTgwOTg3MDA5NzM@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf77 Looking directly into camera breaking fourth wall with smirk",
            "emotional": "\ud83e\udd8a Kneeling at bus stop talking to the Priest: I love you"
        },
        "imdb_id": "tt5687612",
        "imdb_url": "https://www.imdb.com/title/tt5687612/",
        "plot": "A dry-witted woman, known only as Fleabag, has no filter as she navigates life and love in London while trying to cope with tragedy. The angry, grief-riddled woman tries to heal while rejecting anyone who tries to help her, but Fleabag continues to keep up her bravado through it all. Comic actress Phoebe Waller-Bridge stars as the titular character on the series, which is based on Waller-Bridge's 2013 one-woman show of the same name.",
        "actors": "Phoebe Waller-Bridge, Sian Clifford, Olivia Colman",
        "runtime": "2 Seasons \u2022 27 min",
        "rated": "TV-MA",
        "awards": "Won 6 Primetime Emmys. 70 wins & 71 nominations total",
        "metascore": "88",
        "imdb_votes": "245,134",
        "trailer_id": "Nd3Qlo0qspU",
        "clip_url": "https://www.youtube-nocookie.com/embed/Nd3Qlo0qspU",
        "clip_title": "Fleabag - Trailer | Amazon Prime Video",
        "clip_duration": "2:02",
        "sound_theme": "High-Energy Church Choirs & Cheeky Modern Electronic"
    },
    {
        "id": "s_15",
        "title": "The Bear",
        "year": "2022\u20132026",
        "media_type": "series",
        "total_seasons": "5 Seasons",
        "genres": [
            "Comedy",
            "Drama"
        ],
        "director": "Created by Christopher Storer",
        "rating": 8.5,
        "match_keywords": [
            "carmy",
            "yes chef",
            "kitchen",
            "the original beef",
            "chicago"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjk2NWI5OTctODcwYy00NGRmLWFmN2YtOTZiNzFiYjVlODBkXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udd2a Carmy screaming Yes Chef during high-speed dinner ticket rush",
            "emotional": "\ud83e\udd6b Opening the family tomato sauce can finding cash inside"
        },
        "imdb_id": "tt14452776",
        "imdb_url": "https://www.imdb.com/title/tt14452776/",
        "plot": "Carmen Berzatto, a brilliant young chef from the fine-dining world is forced to return home to run his local family sandwich shop - the Original Beef of Chicagoland - after a heartbreaking death in his family. A world away from what he's used to, Carmy must balance the soul-crushing reality of trading in Michelin star restaurants for the small 'business' kitchen filled with strong-willed and obstinate staff and his strained familial relationships, all while grappling with the impact of his brother's suicide.",
        "actors": "Jeremy Allen White, Ebon Moss-Bachrach, Ayo Edebiri",
        "runtime": "5 Seasons \u2022 N/A",
        "rated": "TV-MA",
        "awards": "Won 21 Primetime Emmys. 116 wins & 212 nominations total",
        "metascore": "88",
        "imdb_votes": "315,074",
        "trailer_id": "gBmkI4jlaIo",
        "clip_url": "https://www.youtube-nocookie.com/embed/gBmkI4jlaIo",
        "clip_title": "The Bear Season 1 Trailer",
        "clip_duration": "2:16",
        "sound_theme": "Tense Ticking Stopwatch & Fast Chicago Alt-Rock Beat"
    },
    {
        "id": "s_16",
        "title": "Narcos",
        "year": "2015\u20132017",
        "media_type": "series",
        "total_seasons": "3 Seasons",
        "genres": [
            "Biography",
            "Crime",
            "Drama"
        ],
        "director": "Created by Carlo Bernard & Chris Brancato",
        "rating": 8.7,
        "match_keywords": [
            "pablo escobar",
            "medellin",
            "dea",
            "plata o plomo",
            "cartel"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzQwOTcwMzIwN15BMl5BanBnXkFtZTgwMjYxMTA0NjE@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udcb5 Pablo Escobar counting cash bricks on Medellin ranch",
            "emotional": "\u2615 Plata o Plomo ultimatum at the police checkpoint"
        },
        "imdb_id": "tt2707408",
        "imdb_url": "https://www.imdb.com/title/tt2707408/",
        "plot": "Narcos tells the true-life story of the growth and spread of cocaine drug cartels across the globe and attendant efforts of law enforcement to meet them head on in brutal, bloody conflict. It centers around the notorious Colombian cocaine kingpin Pablo Escobar (Wagner Moura) and Steve Murphy (Holbrook), a DEA agent sent to Colombia on a U.S. mission to capture him and ultimately kill him.",
        "actors": "Pedro Pascal, Wagner Moura, Boyd Holbrook",
        "runtime": "3 Seasons \u2022 49 min",
        "rated": "TV-MA",
        "awards": "Nominated for 3 Primetime Emmys. 8 wins & 22 nominations total",
        "metascore": "88",
        "imdb_votes": "522,089",
        "trailer_id": "xl8zdCY-abw",
        "clip_url": "https://www.youtube-nocookie.com/embed/xl8zdCY-abw",
        "clip_title": "Series Trailer \u2014 Rodrigo Amarante Tuyo & Medellin Congas",
        "clip_duration": "2:10",
        "sound_theme": "Sensual Spanish Bolero Guitar & Deep Latin Congas"
    },
    {
        "id": "s_17",
        "title": "True Detective",
        "year": "2014\u2013",
        "media_type": "series",
        "total_seasons": "5 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Mystery"
        ],
        "director": "Created by Nic Pizzolatto",
        "rating": 8.8,
        "match_keywords": [
            "rust cohle",
            "yellow king",
            "carcosa",
            "louisiana",
            "detectives"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjgwYzA1NWMtNDYyZi00ZGQyLWI5NTktMDYwZjE2OTIwZWEwXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83d\udeac Rust Cohle Lone Star beer can tin man interrogation",
            "emotional": "\ud83c\udf0c Rust looking at starry night sky: The light is winning"
        },
        "imdb_id": "tt2356777",
        "imdb_url": "https://www.imdb.com/title/tt2356777/",
        "plot": "In 2012, Louisiana State Police Detectives Rust Cohle and Martin Hart are brought in to revisit a homicide case they worked in 1995. As the inquiry unfolds in present day through separate interrogations, the two former detectives narrate the story of their investigation, reopening unhealed wounds, and drawing into question their supposed solving of a bizarre ritualistic murder in 1995. The timelines braid and converge in 2012 as each man is pulled back into a world they believed they'd left behind. In learning about each other and their killer, it becomes clear that darkness lives on both sides of the law.",
        "actors": "Vince Vaughn, Colin Farrell, Rachel McAdams",
        "runtime": "5 Seasons \u2022 55 min",
        "rated": "TV-MA",
        "awards": "Won 6 Primetime Emmys. 46 wins & 168 nominations total",
        "metascore": "88",
        "imdb_votes": "745,221",
        "trailer_id": "fVQUcaO4AvE",
        "clip_url": "https://www.youtube-nocookie.com/embed/fVQUcaO4AvE",
        "clip_title": "True Detective - Season 1: Trailer",
        "clip_duration": "2:14",
        "sound_theme": "Dark Americana Desert Rock & Eerie Slide Guitar"
    },
    {
        "id": "s_18",
        "title": "Chernobyl",
        "year": "2019",
        "media_type": "series",
        "total_seasons": "1 Seasons",
        "genres": [
            "Drama",
            "History",
            "Thriller"
        ],
        "director": "Created by Craig Mazin",
        "rating": 9.3,
        "match_keywords": [
            "reactor 4",
            "radiation",
            "pripyat",
            "legasov",
            "graphite"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzU0OTI4YTQtNGQ1ZS00ZjA4LTg3MTMtZjkyZWNjN2RiZDJmXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2622\ufe0f Graphite fire glowing blue ionization beam into night sky",
            "emotional": "\u2696\ufe0f What is the cost of lies? trial speech with red cards"
        },
        "imdb_id": "tt7366338",
        "imdb_url": "https://www.imdb.com/title/tt7366338/",
        "plot": "In April 1986, a huge explosion erupted at the Chernobyl nuclear power station in northern Ukraine. This series follows the stories of the men and women, who tried to contain the disaster, as well as those who gave their lives preventing a subsequent and worse one.",
        "actors": "Jared Harris, Jessie Buckley, Stellan Skarsg\u00e5rd",
        "runtime": "1 Seasons \u2022 330 min",
        "rated": "TV-MA",
        "awards": "Won 10 Primetime Emmys. 87 wins & 60 nominations total",
        "metascore": "88",
        "imdb_votes": "1,031,497",
        "trailer_id": "s9APLXM9Ei8",
        "clip_url": "https://www.youtube-nocookie.com/embed/s9APLXM9Ei8",
        "clip_title": "Series Trailer \u2014 Hildur Gu\u00f0nad\u00f3ttir Nuclear Power Plant Drones",
        "clip_duration": "2:12",
        "sound_theme": "Actual Reactor Room Audio Recordings & Sub-Drone"
    },
    {
        "id": "s_19",
        "title": "Mindhunter",
        "year": "2017\u20132019",
        "media_type": "series",
        "total_seasons": "2 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Mystery",
            "Thriller"
        ],
        "director": "Created by Joe Penhall",
        "rating": 8.6,
        "match_keywords": [
            "fbi",
            "serial killer",
            "profiling",
            "ed kemper",
            "behavioral"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTk4NDA4MGMtNjliOC00MjExLWI1YzctOTc4NWIxM2I1YjM5XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udf99\ufe0f Holden interviewing serial killer at prison glass table",
            "emotional": "\ud83d\udcfc Tape recorder spinning in dark FBI basement office"
        },
        "imdb_id": "tt5290382",
        "imdb_url": "https://www.imdb.com/title/tt5290382/",
        "plot": "Two FBI agents, fighting the departmental stigma of backroom boys - those who try to complicate the status quo of simple Means, Motive, Opportunity (MMO) of crime-solving with academics - work to develop an innovative investigative field incorporating psychology, anthropology and sociology as a method to reveal the motive. They acknowledge classic crime-solving - MMO - as no longer sufficient because criminality is becoming more complicated as Motive graduates from need and greed to inexplicable and irrational reasons. They theorize applying deeper psychological evaluation will posit new questions. Simply, asking Why will lead to the Who. This series focuses on the development by two men, two agents, of a new criminal field and does so through story lines of visiting the sociopathic mind.",
        "actors": "Jonathan Groff, Holt McCallany, Anna Torv",
        "runtime": "2 Seasons \u2022 60 min",
        "rated": "TV-MA",
        "awards": "Nominated for 2 Primetime Emmys. 5 wins & 34 nominations total",
        "metascore": "88",
        "imdb_votes": "391,041",
        "trailer_id": "DHJO6VR6TYY",
        "clip_url": "https://www.youtube-nocookie.com/embed/DHJO6VR6TYY",
        "clip_title": "Mindhunter Season 1 Trailer",
        "clip_duration": "2:08",
        "sound_theme": "Disturbing Mechanical Clocks & Ambient Synth Pads"
    },
    {
        "id": "s_20",
        "title": "Arcane",
        "year": "2021\u20132024",
        "media_type": "series",
        "total_seasons": "2 Seasons",
        "genres": [
            "Animation",
            "Action",
            "Adventure",
            "Sci-Fi"
        ],
        "director": "Created by Christian Linke & Alex Yee",
        "rating": 9.0,
        "match_keywords": [
            "jinx",
            "vi",
            "piltover",
            "zaun",
            "hextech"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYjA2NzhlMDItNWRmZC00MzRjLWE3ZjAtZjBlZDAwOWY2ODdjXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83e\udd4a Vi powered gauntlet boxing duel in Zaun neon alley",
            "emotional": "\ud83d\udd25 Jinx lighting blue flare on smoke tower waiting for Vi"
        },
        "imdb_id": "tt11126994",
        "imdb_url": "https://www.imdb.com/title/tt11126994/",
        "plot": "The delicate balance between the rich city of Piltover and the seedy underbelly of Zaun. Tensions between these city-states boil over with the creation of \"hextech\", a way for any person to control magical energy in Piltover, and in Zaun, a new drug called \"shimmer\" transforms humans into monsters. The rivalry between the cities splits families and friends as Arcane brings life to the relationships that shape some of League of Legends' famous champions including Vi, Jinx, Caitlyn, Jayce, Viktor, and Ekko.",
        "actors": "Kevin Alejandro, Hailee Steinfeld, Ella Purnell",
        "runtime": "2 Seasons \u2022 N/A",
        "rated": "TV-14",
        "awards": "Won 8 Primetime Emmys. 41 wins & 13 nominations total",
        "metascore": "88",
        "imdb_votes": "441,347",
        "trailer_id": "fXmAurh012s",
        "clip_url": "https://www.youtube-nocookie.com/embed/fXmAurh012s",
        "clip_title": "Series Trailer \u2014 Imagine Dragons Enemy & Piltover Synthwave",
        "clip_duration": "2:34",
        "sound_theme": "Hard-Hitting Electronic Rock & Hyper-Stylized Choirs"
    },
    {
        "id": "s_21",
        "title": "Black Mirror",
        "year": "2011\u2013",
        "media_type": "series",
        "total_seasons": "7 Seasons",
        "genres": [
            "Drama",
            "Mystery",
            "Sci-Fi",
            "Thriller"
        ],
        "director": "Created by Charlie Brooker",
        "rating": 8.7,
        "match_keywords": [
            "dystopia",
            "technology",
            "social score",
            "future",
            "anthology"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODcxMWI2NDMtYTc3NC00OTZjLWFmNmUtM2NmY2I1ODkxYzczXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udcf1 Holographic rating stars floating above faces in pastel suburb",
            "emotional": "\ud83d\udcfa Prime Minister broadcast ultimatum across silent London"
        },
        "imdb_id": "tt2085059",
        "imdb_url": "https://www.imdb.com/title/tt2085059/",
        "plot": "Set in a world only minutes from our own, \"Black Mirror\", a UK and USA non-hosted anthology series; unveils how modern technologies can backfire and be used against their makers, every episode set in a slightly different reality with different characters combating different types of technologies.",
        "actors": "Anjana Vasan, Cristin Milioti, Jesse Plemons",
        "runtime": "7 Seasons \u2022 60 min",
        "rated": "TV-MA",
        "awards": "Won 6 Primetime Emmys. 48 wins & 186 nominations total",
        "metascore": "88",
        "imdb_votes": "735,388",
        "trailer_id": "jDiYGjp5iFg",
        "clip_url": "https://www.youtube-nocookie.com/embed/jDiYGjp5iFg",
        "clip_title": "Series Trailer \u2014 Black Mirror Broken Glass & Digital Glitch",
        "clip_duration": "2:05",
        "sound_theme": "High-Pitched Digital Sine Wave & Sudden Glitch Drop"
    },
    {
        "id": "s_22",
        "title": "Ted Lasso",
        "year": "2020\u2013",
        "media_type": "series",
        "total_seasons": "4 Seasons",
        "genres": [
            "Comedy",
            "Drama",
            "Sport"
        ],
        "director": "Created by Brendan Hunt & Joe Kelly",
        "rating": 8.7,
        "match_keywords": [
            "afc richmond",
            "believe",
            "biscuits",
            "coach",
            "wholesome"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BM2ZlYTU0YWUtMzY4OC00N2JkLTk1ZGQtN2UxNWJhMTBkMzM4XkEyXkFqcGc@._V1_QL75_UY562_CR35,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u26bd Ted pinning yellow BELIEVE sign above AFC Richmond locker door",
            "emotional": "\ud83c\udf6a Handing pink box of homemade shortbread biscuits to Rebecca"
        },
        "imdb_id": "tt10986410",
        "imdb_url": "https://www.imdb.com/title/tt10986410/",
        "plot": "In a shock development struggling English Premier League team AFC Richmond hires American football coach Ted Lasso as its new manager. Lasso knows nothing about soccer/football. With unshakable enthusiasm and positivity he rises to the challenge but little known to him there are forces within the club that don't want him to succeed.",
        "actors": "Jason Sudeikis, Hannah Waddingham, Jeremy Swift",
        "runtime": "4 Seasons \u2022 30 min",
        "rated": "TV-MA",
        "awards": "Won 13 Primetime Emmys. 75 wins & 213 nominations total",
        "metascore": "88",
        "imdb_votes": "464,037",
        "trailer_id": "3u7EIiohs6U",
        "clip_url": "https://www.youtube-nocookie.com/embed/3u7EIiohs6U",
        "clip_title": "Ted Lasso \u2014 Official Trailer",
        "clip_duration": "2:12",
        "sound_theme": "Joyful Whistled Indie Folk & Upbeat Acoustic Strumming"
    },
    {
        "id": "s_23",
        "title": "The Last of Us",
        "year": "2023\u2013",
        "media_type": "series",
        "total_seasons": "3 Seasons",
        "genres": [
            "Action",
            "Adventure",
            "Drama",
            "Sci-Fi"
        ],
        "director": "Created by Craig Mazin & Neil Druckmann",
        "rating": 8.4,
        "match_keywords": [
            "cordyceps",
            "joel",
            "ellie",
            "clickers",
            "fireflies"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYWI3ODJlMzktY2U5NC00ZjdlLWE1MGItNWQxZDk3NWNjN2RhXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83c\udf3f Joel and Ellie riding horses through overgrown post-apocalyptic Boston",
            "emotional": "\ud83e\udd92 Feeding tall giraffe on rooftop overlooking city ruins"
        },
        "imdb_id": "tt3581920",
        "imdb_url": "https://www.imdb.com/title/tt3581920/",
        "plot": "20 years after modern civilization has been destroyed, Joel, a hardened survivor, is hired to smuggle Ellie, a 14-year-old girl, out of an oppressive quarantine zone. What starts as a small job soon becomes a brutal heartbreaking journey as they both must traverse the U.S. and depend on each other for survival.",
        "actors": "Bella Ramsey, Pedro Pascal, Gabriel Luna",
        "runtime": "3 Seasons \u2022 18S min",
        "rated": "TV-MA",
        "awards": "Won 9 Primetime Emmys. 110 wins & 208 nominations total",
        "metascore": "88",
        "imdb_votes": "749,733",
        "trailer_id": "uLtkt8BonwM",
        "clip_url": "https://www.youtube-nocookie.com/embed/uLtkt8BonwM",
        "clip_title": "Series Trailer \u2014 Gustavo Santaolalla Charango & Clicker Screech",
        "clip_duration": "2:28",
        "sound_theme": "Intimate Gustavo Ronroco Acoustic Plucks & Chilling Strings"
    },
    {
        "id": "s_24",
        "title": "Suits",
        "year": "2011\u20132019",
        "media_type": "series",
        "total_seasons": "9 Seasons",
        "genres": [
            "Comedy",
            "Drama"
        ],
        "director": "Created by Aaron Korsh",
        "rating": 8.4,
        "match_keywords": [
            "harvey specter",
            "mike ross",
            "pearson hardman",
            "lawyer",
            "corporate"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYmE4MmNjZjUtNTEyNy00NTZiLWE4NTktYjM2NjBhYzQ1N2IzXkEyXkFqcGc@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udc54 Harvey Specter closing multi-million corporate merger deal",
            "emotional": "\ud83d\udcbc Mike Ross reciting law statutes with photographic memory"
        },
        "imdb_id": "tt1632701",
        "imdb_url": "https://www.imdb.com/title/tt1632701/",
        "plot": "Big-time Manhattan corporate lawyer Harvey Specter and his team, which includes Donna Paulsen, Louis Litt, and Alex Williams, are launched into a play for power when a new partner joins the firm. With his two best associates gone and Jessica back in Chicago, Specter and the team try to adjust to a new normal without them. The team faces down betrayals, fiery relationships, and secrets that eventually come to light. Old and new rivalries surface among members of the team as they learn to deal with their new member.",
        "actors": "Gabriel Macht, Patrick J. Adams, Meghan Markle",
        "runtime": "9 Seasons \u2022 44 min",
        "rated": "TV-14",
        "awards": "1 win & 9 nominations total",
        "metascore": "88",
        "imdb_votes": "549,151",
        "trailer_id": "85z53bAebsI",
        "clip_url": "https://www.youtube-nocookie.com/embed/85z53bAebsI",
        "clip_title": "Series Trailer \u2014 Greenback Boogie by Ima Robot & Manhattan Horns",
        "clip_duration": "2:06",
        "sound_theme": "Catchy Indie Rock Groove & Snappy Manhattan Claps"
    },
    {
        "id": "s_25",
        "title": "Dexter",
        "year": "2006\u20132013",
        "media_type": "series",
        "total_seasons": "8 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Mystery"
        ],
        "director": "Created by James Manos Jr.",
        "rating": 8.6,
        "match_keywords": [
            "blood splatter",
            "bay harbor butcher",
            "code of harry",
            "miami",
            "dark passenger"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ3YmQ4YzMtOTkyZC00YmM5LThhZjEtM2E0MjFkNTc0OGJhXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83e\ude78 Dexter taking single blood slide drop in plastic kill room",
            "emotional": "\ud83d\udee5\ufe0f Slice of Life boat cruising into Miami moonlight ocean"
        },
        "imdb_id": "tt0773262",
        "imdb_url": "https://www.imdb.com/title/tt0773262/",
        "plot": "He's smart, he's good looking, and he's got a great sense of humor. He's Dexter Morgan, everyone's favorite serial killer. As a Miami forensics expert, he spends his days solving crimes, and nights committing them. But Dexter lives by a strict code of honor that is both his saving grace and lifelong burden. Torn between his deadly compulsion and his desire for true happiness, Dexter is a man in profound conflict with the world and himself. Golden Globe winner Michael C. Hall stars in the hit SHOWTIME Original Series.",
        "actors": "Michael C. Hall, Jennifer Carpenter, David Zayas",
        "runtime": "8 Seasons \u2022 53 min",
        "rated": "TV-MA",
        "awards": "Won 4 Primetime Emmys. 56 wins & 202 nominations total",
        "metascore": "88",
        "imdb_votes": "914,526",
        "trailer_id": "YQeUmSD1c3g",
        "clip_url": "https://www.youtube-nocookie.com/embed/YQeUmSD1c3g",
        "clip_title": "Dexter (2006) Official Trailer",
        "clip_duration": "2:04",
        "sound_theme": "Latin Percussion & Plucked Island Marimba with Saw"
    },
    {
        "id": "s_26",
        "title": "The Office",
        "year": "2005\u20132013",
        "media_type": "series",
        "total_seasons": "9 Seasons",
        "genres": [
            "Comedy"
        ],
        "director": "Created by Greg Daniels & Ricky Gervais",
        "rating": 9.0,
        "match_keywords": [
            "dunder mifflin",
            "michael scott",
            "dwight schrute",
            "jim pam",
            "scranton"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjQwYzBlYzUtZjhhOS00ZDQ0LWE0NzAtYTk4MjgzZTNkZWEzXkEyXkFqcGc@._V1_QL75_UX380_CR0,4,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udcce Jim placing Dwight stapler in yellow Jell-O mold",
            "emotional": "\ud83c\udfc6 World's Best Boss mug toast in Dunder Mifflin kitchen"
        },
        "imdb_id": "tt0386676",
        "imdb_url": "https://www.imdb.com/title/tt0386676/",
        "plot": "A mediocre paper company in the hands of Scranton, PA branch manager Michael Scott. This mockumentary follows the everyday lives of the manager and the employees he \"manages.\" The crew follows the employees around 24/7 and captures their quite humorous and bizarre encounters as they will do what it takes to keep the company thriving.",
        "actors": "Steve Carell, Jenna Fischer, John Krasinski",
        "runtime": "9 Seasons \u2022 22 min",
        "rated": "TV-14",
        "awards": "Won 5 Primetime Emmys. 61 wins & 211 nominations total",
        "metascore": "88",
        "imdb_votes": "828,915",
        "trailer_id": "LHOtME2DL4g",
        "clip_url": "https://www.youtube-nocookie.com/embed/LHOtME2DL4g",
        "clip_title": "Series Trailer \u2014 Scrantones Accordion Melody & Melodica",
        "clip_duration": "1:45",
        "sound_theme": "Uplifting Melodica & Funky TV Comedy Rock Band"
    },
    {
        "id": "s_27",
        "title": "Friends",
        "year": "1994\u20132004",
        "media_type": "series",
        "total_seasons": "10 Seasons",
        "genres": [
            "Comedy",
            "Romance"
        ],
        "director": "Created by David Crane & Marta Kauffman",
        "rating": 8.8,
        "match_keywords": [
            "central perk",
            "chandler",
            "joey",
            "rachel",
            "monica"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTU2YmM5ZjctOGVlMC00YTczLTljM2MtYjhlNGI5YWMyZjFkXkEyXkFqcGc@._V1_QL75_UY562_CR1,0,380,562_.jpg",
        "poster_variants": {
            "action": "\ud83d\udecb\ufe0f Moving brown couch up narrow stairs: PIVOT! PIVOT!",
            "emotional": "\u2615 Six friends sitting together on orange couch in Central Perk"
        },
        "imdb_id": "tt0108778",
        "imdb_url": "https://www.imdb.com/title/tt0108778/",
        "plot": "Ross Geller, Rachel Green, Monica Geller, Joey Tribbiani, Chandler Bing, and Phoebe Buffay are six twenty-somethings living in New York City. Over the course of 10 years and seasons, these friends go through life lessons, family, love, drama, friendship, and comedy.",
        "actors": "Jennifer Aniston, Courteney Cox, Lisa Kudrow",
        "runtime": "10 Seasons \u2022 22 min",
        "rated": "TV-14",
        "awards": "Won 6 Primetime Emmys. 79 wins & 231 nominations total",
        "metascore": "88",
        "imdb_votes": "1,189,336",
        "trailer_id": "RasWhgd4vao",
        "clip_url": "https://www.youtube-nocookie.com/embed/RasWhgd4vao",
        "clip_title": "Friends: The Reunion Trailer",
        "clip_duration": "2:02",
        "sound_theme": "The Rembrandts 90s Pop Rock & Four Iconic Claps"
    },
    {
        "id": "s_28",
        "title": "Brooklyn Nine-Nine",
        "year": "2013\u20132021",
        "media_type": "series",
        "total_seasons": "8 Seasons",
        "genres": [
            "Comedy",
            "Crime"
        ],
        "director": "Created by Dan Goor & Michael Schur",
        "rating": 8.4,
        "match_keywords": [
            "jake peralta",
            "captain holt",
            "99th precinct",
            "title of your sex tape",
            "cool cool cool"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzBiODQxZTUtNjc0MC00Yzc1LThmYTMtN2YwYTU3NjgxMmI4XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udfa4 Lineup singing I Want It That Way in interrogation room",
            "emotional": "\ud83d\ude93 Holt smiling proudly at Jake: You are a great detective"
        },
        "imdb_id": "tt2467372",
        "imdb_url": "https://www.imdb.com/title/tt2467372/",
        "plot": "Captain Ray Holt takes over Brooklyn's 99th precinct, which includes Detective Jake Peralta, a talented but carefree detective who's used to doing whatever he wants. The other employees of the 99th precinct include Detective Amy Santiago, Jake's over achieving and competitive partner; Detective Rosa Diaz, a tough and kept to herself coworker; Detective Charles Boyle, Jake's best friend who also has crush on Rosa; Detective Sergeant Terry Jeffords, who was recently taken off the field after the birth of his twin girls; and Gina Linetti, the precinct's sarcastic administrator.",
        "actors": "Andy Samberg, Stephanie Beatriz, Terry Crews",
        "runtime": "8 Seasons \u2022 22 min",
        "rated": "TV-14",
        "awards": "Won 2 Primetime Emmys. 19 wins & 129 nominations total",
        "metascore": "88",
        "imdb_votes": "412,257",
        "trailer_id": "sEOuJ4z5aTc",
        "clip_url": "https://www.youtube-nocookie.com/embed/sEOuJ4z5aTc",
        "clip_title": "Series Trailer \u2014 Dan Marocco Cop Show Brass & Slap Bass",
        "clip_duration": "1:48",
        "sound_theme": "Punchy Funk Brass Fanfare & Upbeat Drum Groove"
    },
    {
        "id": "s_29",
        "title": "Vikings",
        "year": "2013\u20132020",
        "media_type": "series",
        "total_seasons": "6 Seasons",
        "genres": [
            "Action",
            "Adventure",
            "Drama",
            "History"
        ],
        "director": "Created by Michael Hirst",
        "rating": 8.5,
        "match_keywords": [
            "ragnar lothbrok",
            "valhalla",
            "shieldmaiden",
            "kattegat",
            "longships"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTFmZmExYTEtYmE0Mi00MzRmLWE4ZDYtOThiNzNlOTIyODljXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\u2694\ufe0f Ragnar Lothbrok raiding English coast in wooden longships",
            "emotional": "\ud83e\udd85 Ragnar sitting on seaside cliff talking to raven"
        },
        "imdb_id": "tt2306299",
        "imdb_url": "https://www.imdb.com/title/tt2306299/",
        "plot": "The adventures of a Ragnar Lothbrok: the greatest hero of his age. The series tells the saga of Ragnar's band of Viking brothers and his family as he rises to become King of the Viking tribes. As well as being a fearless warrior, Ragnar embodies the Norse traditions of devotion to the gods: legend has it that he was a direct descendant of Odin, the god of war and warriors.",
        "actors": "Katheryn Winnick, Gustaf Skarsg\u00e5rd, Alexander Ludwig",
        "runtime": "6 Seasons \u2022 44 min",
        "rated": "TV-MA",
        "awards": "Won 1 Primetime Emmy. 46 wins & 133 nominations total",
        "metascore": "88",
        "imdb_votes": "636,827",
        "trailer_id": "9GgxinPwAGc",
        "clip_url": "https://www.youtube-nocookie.com/embed/9GgxinPwAGc",
        "clip_title": "Series Trailer \u2014 Wardruna Norse Horns & Fever Ray If I Had A Heart",
        "clip_duration": "2:15",
        "sound_theme": "Deep Scandinavian Shamanic Chants & Nordic Tagelharpa"
    },
    {
        "id": "s_30",
        "title": "Loki",
        "year": "2021\u20132023",
        "media_type": "series",
        "total_seasons": "2 Seasons",
        "genres": [
            "Action",
            "Adventure",
            "Fantasy",
            "Sci-Fi"
        ],
        "director": "Created by Michael Waldron",
        "rating": 8.2,
        "match_keywords": [
            "tva",
            "multiverse",
            "god of stories",
            "mobius",
            "timelines"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA2YjM2ZWQtYTZhMS00OTI3LTlhYzQtZjBiZWZkMDdlNjA5XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u23f3 Loki weaving glowing green temporal timeline strands",
            "emotional": "\ud83d\udc51 For you, for all of us: ascending to the temporal throne"
        },
        "imdb_id": "tt9140554",
        "imdb_url": "https://www.imdb.com/title/tt9140554/",
        "plot": "When an alternate Loki uses the Tesseract to escape in \"Avengers: Endgame,\" the Time Variance Authority (TVA), a group that keeps an eye on the sacred timeline, captures him. After first doubting the TVA's legitimacy, Loki is forced to decide between being eliminated from the universe and assisting them in their search for a hazardous time variant-a different version of himself going by the name Sylvie. Along the way, they discover the secrets of the TVA and travel across time, forcing Loki to wrestle with issues of free will and identity and make a decision that could destroy the sacred timeline and unleash havoc over the multiverse.",
        "actors": "Tom Hiddleston, Owen Wilson, Sophia Di Martino",
        "runtime": "2 Seasons \u2022 N/A",
        "rated": "TV-14",
        "awards": "Nominated for 9 Primetime Emmys. 16 wins & 97 nominations total",
        "metascore": "88",
        "imdb_votes": "470,715",
        "trailer_id": "nW948Va-l10",
        "clip_url": "https://www.youtube-nocookie.com/embed/nW948Va-l10",
        "clip_title": "Series Trailer \u2014 Natalie Holt Theremin & Glorious Purpose",
        "clip_duration": "2:22",
        "sound_theme": "Eerie Sci-Fi Theremin & Massive Marvel Brass Crescendo"
    },
    {
        "id": "s_31",
        "title": "Sh\u014dgun",
        "year": "2024\u20132026",
        "media_type": "series",
        "total_seasons": "3 Seasons",
        "genres": [
            "Adventure",
            "Drama",
            "History"
        ],
        "director": "Created by Rachel Kondo & Justin Marks",
        "rating": 8.6,
        "match_keywords": [
            "toranaga",
            "samurai",
            "blackthorne",
            "mariko",
            "feudal japan"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZmJkMDRjYzEtMWI3Ny00OWE3LWJlNTItMGQ1MTQzMzc3NDY5XkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\u2694\ufe0f Toranaga samurai cavalry charge in mist dawn forest",
            "emotional": "\ud83c\udf38 Tea ceremony under blooming sakura blossoms in Osaka castle"
        },
        "imdb_id": "tt2788316",
        "imdb_url": "https://www.imdb.com/title/tt2788316/",
        "plot": "Set in the 17th Century, the story is told from the perspective of British hero John Blackthorne, a sailor who rises from outsider to samurai, while being used as a pawn in Japanese leader Toranaga's struggle to reach the top of the ruling chain, or Shogun.",
        "actors": "Cosmo Jarvis, Hiroyuki Sanada, Anna Sawai",
        "runtime": "3 Seasons \u2022 N/A",
        "rated": "TV-MA",
        "awards": "Won 18 Primetime Emmys. 92 wins & 76 nominations total",
        "metascore": "88",
        "imdb_votes": "240,464",
        "trailer_id": "yAN5uspO_hk",
        "clip_url": "https://www.youtube-nocookie.com/embed/yAN5uspO_hk",
        "clip_title": "Sh\u014dgun - Official Trailer",
        "clip_duration": "2:26",
        "sound_theme": "Deep Wooden Shakuhachi Flutes & Explosive War Drums"
    },
    {
        "id": "s_32",
        "title": "Fargo",
        "year": "2014\u20132024",
        "media_type": "series",
        "total_seasons": "5 Seasons",
        "genres": [
            "Crime",
            "Drama",
            "Thriller"
        ],
        "director": "Created by Noah Hawley",
        "rating": 8.9,
        "match_keywords": [
            "lorne malvo",
            "minnesota",
            "snow",
            "coen brothers",
            "heist"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNTUxOGQxYjMtYWI5NS00YTljLWE3MTItODczYTRlYTI3OWRiXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\u2744\ufe0f Lorne Malvo standing in snow blizzard outside motel room",
            "emotional": "\ud83e\ude78 Red blood trail across white frozen Minnesota lake"
        },
        "imdb_id": "tt2802850",
        "imdb_url": "https://www.imdb.com/title/tt2802850/",
        "plot": "Various chronicles of deception, intrigue, and murder in and around frozen Minnesota. Yet all of these tales mysteriously lead back one way or another to Fargo, North Dakota.",
        "actors": "Billy Bob Thornton, Martin Freeman, Allison Tolman, Colin Hanks, Chris Rock, Juno Temple",
        "runtime": "5 Seasons \u2022 53 min/ep",
        "rated": "R",
        "awards": "Won 6 Primetime Emmys. 58 wins & 240 nominations total",
        "metascore": "88",
        "imdb_votes": "780,547",
        "trailer_id": "setgvHG3w48",
        "clip_url": "https://www.youtube-nocookie.com/embed/setgvHG3w48",
        "clip_title": "Fargo | Trailer",
        "clip_duration": "2:08",
        "sound_theme": "Bleak Minnesota Strings & Quirky Melancholic Harp"
    },
    {
        "id": "s_33",
        "title": "Attack on Titan",
        "year": "2013\u20132023",
        "media_type": "series",
        "total_seasons": "4 Seasons",
        "genres": [
            "Animation",
            "Action",
            "Adventure",
            "Fantasy"
        ],
        "director": "Created by Hajime Isayama",
        "rating": 9.1,
        "match_keywords": [
            "levi ackerman",
            "eren yeager",
            "scout regiment",
            "titans",
            "walls"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjliODY5MzQtMmViZC00MTZmLWFhMWMtMjMwM2I3OGY1MTRiXkEyXkFqcGc@._V1_QL75_UY562_CR9,0,380,562_.jpg",
        "poster_variants": {
            "action": "\u2694\ufe0f Levi Ackerman ODM gear spinning blade whirlwind against Beast Titan",
            "emotional": "\ud83c\udf05 Eren and Armin looking at the vast endless blue sea"
        },
        "imdb_id": "tt2560140",
        "imdb_url": "https://www.imdb.com/title/tt2560140/",
        "plot": "Humans are nearly exterminated by giant creatures called Titans. Titans are typically several stories tall, seem to have no intelligence, devour human beings and, worst of all, seem to do it for the pleasure rather than as a food source. A small percentage of humanity survived by walling themselves in a land protected by extremely high walls, even taller than the biggest of titans. Flash forward to the present, and mankind has not seen a titan in over 100 years. One day, 10 year old Eren and his childhood friend Mikasa witness something horrific as the city walls are destroyed by a colossal titan that appears out of thin air. As the smaller titans flood the city, the two kids watch in horror as Eren's mother is eaten alive. Eren vows that he will murder every single titan and take revenge for all of mankind.",
        "actors": "Jessie James Grelle, Bryce Papenbrook, Trina Nishimura",
        "runtime": "4 Seasons \u2022 24 min",
        "rated": "TV-MA",
        "awards": "42 wins & 88 nominations total",
        "metascore": "88",
        "imdb_votes": "746,262",
        "trailer_id": "MGRm4IzK1SQ",
        "clip_url": "https://www.youtube-nocookie.com/embed/MGRm4IzK1SQ",
        "clip_title": "Series Trailer \u2014 Hiroyuki Sawano Guren no Yumiya & Titan Roar",
        "clip_duration": "2:36",
        "sound_theme": "Blazing Symphonic Metal Guitars & German Choral Fanfare"
    },
    {
        "id": "s_34",
        "title": "Death Note",
        "year": "2006\u20132007",
        "media_type": "series",
        "total_seasons": "1 Seasons",
        "genres": [
            "Animation",
            "Crime",
            "Drama",
            "Mystery"
        ],
        "director": "Created by Tsugumi Ohba",
        "rating": 8.9,
        "match_keywords": [
            "light yagami",
            "l",
            "ryuk",
            "shinigami",
            "kiras"
        ],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BYTgyZDhmMTEtZDFhNi00MTc4LTg3NjUtYWJlNGE5Mzk2NzMxXkEyXkFqcGc@._V1_SX300.jpg",
        "poster_variants": {
            "action": "\ud83c\udf4e Ryuk floating in room as Light writes in Death Note with pen",
            "emotional": "\ud83e\udd54 I'll take a potato chip... and eat it!"
        },
        "imdb_id": "tt0877057",
        "imdb_url": "https://www.imdb.com/title/tt0877057/",
        "plot": "After an intelligent yet cynical high school student begins to cleanse the world from evil with the help of a magical notebook that can kill anyone whose name is written on it, international authorities call upon a mysterious detective known as \"L\" to thwart his efforts.",
        "actors": "Mamoru Miyano, Brad Swaile, Vincent Tong",
        "runtime": "1 Seasons \u2022 24 min",
        "rated": "TV-14",
        "awards": "2 wins & 1 nomination total",
        "metascore": "88",
        "imdb_votes": "466,043",
        "trailer_id": "NlJZ-YgAt-c",
        "clip_url": "https://www.youtube-nocookie.com/embed/NlJZ-YgAt-c",
        "clip_title": "Series Trailer \u2014 Yoshihisa Hirano L's Theme Piano & Death Chants",
        "clip_duration": "2:12",
        "sound_theme": "Iconic Two-Note Rock Piano Melody & Gothic Gregorian Chants"
    },
    {
            "id": "m_91",
            "title": "Anyone But You",
            "year": 2023,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Will Gluck",
            "rating": 6.4,
            "match_keywords": [
                    "fake dating",
                    "Sydney",
                    "Australia",
                    "enemies to lovers"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMjYwOTg4Y2YtNmY3My00NTdhLWExNWQtNDM1ODNmMWVkMDc3XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Sydney opera house sunrise breeze",
                    "emotional": "🌹 Unwritten acoustic guitar & Australian beach vibes"
            },
            "imdb_id": "tt26047818",
            "imdb_url": "https://www.imdb.com/title/tt26047818/",
            "plot": "After an amazing first date, Bea and Ben's fiery attraction turns ice cold - until they find themselves unexpectedly reunited at a destination wedding in Australia. So they do what any two mature adults would do: pretend to be a couple.",
            "actors": "Sydney Sweeney, Glen Powell, Alexandra Shipp",
            "runtime": "103 min",
            "rated": "R",
            "awards": "Won 1 People's Choice Award. 4 nominations total",
            "metascore": "52",
            "imdb_votes": "125,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "7HMKFy3FvW8",
            "clip_url": "https://www.youtube-nocookie.com/embed/7HMKFy3FvW8",
            "clip_title": "Anyone But You | Official Teaser Trailer | Sydney Sweeney, Glen Powell",
            "clip_duration": "2:35",
            "sound_theme": "Sun-Kissed Pop Guitar & Australian Beach Waves"
    },
    {
            "id": "m_92",
            "title": "How to Lose a Guy in 10 Days",
            "year": 2003,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Donald Petrie",
            "rating": 6.5,
            "match_keywords": [
                    "magazine",
                    "advertising",
                    "bet",
                    "Manhattan"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMjE4NTA1NzExN15BMl5BanBnXkFtZTYwNjc3MjM3._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Yellow silk evening gown at diamond gala",
                    "emotional": "🌹 Knicks basketball court kiss in Madison Square Garden"
            },
            "imdb_id": "tt0326938",
            "imdb_url": "https://www.imdb.com/title/tt0326938/",
            "plot": "Benjamin Barry is an advertising executive and ladies' man who, to win a big campaign, bets that he can make a woman fall in love with him in 10 days. Andie Anderson covers the 'How To' beat for 'Composure' magazine and is assigned to write on how to lose a guy in 10 days.",
            "actors": "Kate Hudson, Matthew McConaughey, Kathryn Hahn",
            "runtime": "116 min",
            "rated": "PG-13",
            "awards": "Won 1 BMI Film Music Award. 6 nominations total",
            "metascore": "45",
            "imdb_votes": "248,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "2ZMGk_Ml1fc",
            "clip_url": "https://www.youtube-nocookie.com/embed/2ZMGk_Ml1fc",
            "clip_title": "How to Lose a Guy in 10 Days (2003) Official Trailer #1 - Kate Hudson Movie HD",
            "clip_duration": "2:24",
            "sound_theme": "Upbeat 2000s Rom-Com Brass & Catchy Pop Funk"
    },
    {
            "id": "m_93",
            "title": "The Holiday",
            "year": 2006,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Nancy Meyers",
            "rating": 6.9,
            "match_keywords": [
                    "home exchange",
                    "England",
                    "Los Angeles",
                    "Christmas"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMTI1MDk0MTIzMV5BMl5BanBnXkFtZTcwNzQzMzkzMQ@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Snowbound cozy English country cottage fireplace",
                    "emotional": "🌹 Film scoring piano duet in Los Angeles sunlit kitchen"
            },
            "imdb_id": "tt0457939",
            "imdb_url": "https://www.imdb.com/title/tt0457939/",
            "plot": "Two women troubled with guy-problems swap homes in each other's countries, where they each meet a local guy and fall in love. Amanda Woods goes to a cozy snowy cottage in Surrey, while Iris Simpkins stays in a luxury mansion in Los Angeles.",
            "actors": "Cameron Diaz, Kate Winslet, Jude Law, Jack Black",
            "runtime": "136 min",
            "rated": "PG-13",
            "awards": "Won 1 Teen Choice Award. 4 nominations total",
            "metascore": "52",
            "imdb_votes": "310,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "wk9caHO3pW0",
            "clip_url": "https://www.youtube-nocookie.com/embed/wk9caHO3pW0",
            "clip_title": "THE HOLIDAY [2006] - Official Trailer (HD)",
            "clip_duration": "2:28",
            "sound_theme": "Hans Zimmer Warm Acoustic Strings & Festive Piano"
    },
    {
            "id": "m_94",
            "title": "Love Actually",
            "year": 2003,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Richard Curtis",
            "rating": 7.6,
            "match_keywords": [
                    "holiday",
                    "ensemble",
                    "London",
                    "airport"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMTY4NjQ5NDc0Nl5BMl5BanBnXkFtZTYwNjk5NDM3._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Cardboard cue card confession in winter snow",
                    "emotional": "🌹 Heathrow Airport arrival lounge reunion hugs"
            },
            "imdb_id": "tt0314331",
            "imdb_url": "https://www.imdb.com/title/tt0314331/",
            "plot": "Follows the lives of eight very different couples in dealing with their love in various loosely interrelated tales all set during a frantic month before Christmas in London, England.",
            "actors": "Hugh Grant, Martine McCutcheon, Liam Neeson, Colin Firth",
            "runtime": "135 min",
            "rated": "R",
            "awards": "Nominated for 2 Golden Globes. 10 wins & 27 nominations",
            "metascore": "55",
            "imdb_votes": "530,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "H9Z3_ifFheQ",
            "clip_url": "https://www.youtube-nocookie.com/embed/H9Z3_ifFheQ",
            "clip_title": "Love Actually (2003) Official Trailer - Colin Firth, Emma Thompson Movie HD",
            "clip_duration": "2:25",
            "sound_theme": "Craig Armstrong Lush London Strings & Pop Horns"
    },
    {
            "id": "m_95",
            "title": "Pretty Woman",
            "year": 1990,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Garry Marshall",
            "rating": 7.1,
            "match_keywords": [
                    "Rodeo Drive",
                    "Beverly Hills",
                    "opera",
                    "fairy tale"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNjk2ODQzNDYxNV5BMl5BanBnXkFtZTgwMTcyNDg4NjE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Red opera gown with laughing jewelry box snap",
                    "emotional": "🌹 Limousine sunroof ride with classical roses"
            },
            "imdb_id": "tt0100405",
            "imdb_url": "https://www.imdb.com/title/tt0100405/",
            "plot": "A man in a legal but hurtful business needs an escort for some social events, and hires a beautiful prostitute he meets on Hollywood Boulevard, only to fall in love with her over a magical week in Beverly Hills.",
            "actors": "Richard Gere, Julia Roberts, Jason Alexander",
            "runtime": "119 min",
            "rated": "R",
            "awards": "Nominated for 1 Oscar. 9 wins & 12 nominations",
            "metascore": "51",
            "imdb_votes": "360,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "2EBAVoN8L_U",
            "clip_url": "https://www.youtube-nocookie.com/embed/2EBAVoN8L_U",
            "clip_title": "Pretty Woman (1990) Trailer #1 | Movieclips Classic Trailers",
            "clip_duration": "2:30",
            "sound_theme": "Roy Orbison Classic Rock Riffs & James Newton Howard Piano"
    },
    {
            "id": "m_96",
            "title": "Clueless",
            "year": 1995,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Amy Heckerling",
            "rating": 6.9,
            "match_keywords": [
                    "high school",
                    "Beverly Hills",
                    "makeover",
                    "90s fashion"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNTBmNTFiYzUtYWQ5Yy00MTY1LWE2YjktYmRlMzAwMTg3OGE1XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Yellow plaid blazer on Beverly Hills boulevard",
                    "emotional": "🌹 Romantic water fountain fountain stairs epiphany"
            },
            "imdb_id": "tt0112697",
            "imdb_url": "https://www.imdb.com/title/tt0112697/",
            "plot": "Shallow, rich and socially successful Cher is at the top of her Beverly Hills high school's pecking scale. Seeing herself as a matchmaker, Cher first coaxes two teachers into dating each other, and then tries to give a klutzy new student a makeover.",
            "actors": "Alicia Silverstone, Paul Rudd, Stacey Dash, Brittany Murphy",
            "runtime": "97 min",
            "rated": "PG-13",
            "awards": "Nominated for 1 BAFTA. 8 wins & 14 nominations",
            "metascore": "68",
            "imdb_votes": "240,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "Mgjwq1ZzdPQ",
            "clip_url": "https://www.youtube-nocookie.com/embed/Mgjwq1ZzdPQ",
            "clip_title": "Clueless (1995) Trailer #1 | Movieclips Classic Trailers",
            "clip_duration": "2:15",
            "sound_theme": "90s Pop-Punk Guitars & Supergrass Grooves"
    },
    {
            "id": "m_97",
            "title": "The Proposal",
            "year": 2009,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Anne Fletcher",
            "rating": 6.8,
            "match_keywords": [
                    "fake engagement",
                    "boss",
                    "Alaska",
                    "immigration"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BOGM5YTNiYzktNmEwOS00OTk4LTkyNjgtMTQyZTU3NTlmZDM3XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Alaskan fjord boat ride surrounded by snowcaps",
                    "emotional": "🌹 Get Low tribal chant dance around forest bonfire"
            },
            "imdb_id": "tt1041829",
            "imdb_url": "https://www.imdb.com/title/tt1041829/",
            "plot": "A pushy Canadian book editor facing deportation forces her young executive assistant to marry her in order to keep her visa status in the U.S., leading to a hilarious trip to his quirky family home in Sitka, Alaska.",
            "actors": "Sandra Bullock, Ryan Reynolds, Mary Steenburgen, Betty White",
            "runtime": "108 min",
            "rated": "PG-13",
            "awards": "Nominated for 1 Golden Globe. 7 wins & 20 nominations",
            "metascore": "48",
            "imdb_votes": "350,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "jHraHCjK094",
            "clip_url": "https://www.youtube-nocookie.com/embed/jHraHCjK094",
            "clip_title": "The Proposal (2009) Trailer #1 | Movieclips Classic Trailers",
            "clip_duration": "2:20",
            "sound_theme": "Upbeat Acoustic Pop & Alaskan Mountain Strings"
    },
    {
            "id": "m_98",
            "title": "Set It Up",
            "year": 2018,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Claire Scanlon",
            "rating": 6.5,
            "match_keywords": [
                    "assistants",
                    "matchmaking",
                    "Manhattan",
                    "workaholic"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA5ZTMyN2YtMjFiNS00ZjE2LTg3NTEtMTQ4ODJjYzg4YTVmXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Rooftop pizza slice date under Manhattan skyline",
                    "emotional": "🌹 Elevator breakdown accidental moment of warmth"
            },
            "imdb_id": "tt4014206",
            "imdb_url": "https://www.imdb.com/title/tt4014206/",
            "plot": "Two overworked and underpaid assistants in New York City realize they can make their lives easier if they team up to trick their demanding workaholic bosses into falling in love with each other.",
            "actors": "Zoey Deutch, Glen Powell, Lucy Liu, Taye Diggs",
            "runtime": "117 min",
            "rated": "TV-14",
            "awards": "Nominated for 1 Artios Award. 2 nominations total",
            "metascore": "62",
            "imdb_votes": "65,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "X-eRc9PF3TU",
            "clip_url": "https://www.youtube-nocookie.com/embed/X-eRc9PF3TU",
            "clip_title": "Set It Up | Official Trailer [HD] | Netflix",
            "clip_duration": "2:18",
            "sound_theme": "Breezy Manhattan Indie Pop & Snappy Brass"
    },
    {
            "id": "m_99",
            "title": "50 First Dates",
            "year": 2004,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Peter Segal",
            "rating": 6.8,
            "match_keywords": [
                    "Hawaii",
                    "amnesia",
                    "sea life",
                    "first date"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAwMzc4MDcxNF5BMl5BanBnXkFtZTYwOTYzMzQ3._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Hawaiian beach waffle house drawing scene",
                    "emotional": "🌹 Morning videotape revelation with sailing yacht in Alaska"
            },
            "imdb_id": "tt0343660",
            "imdb_url": "https://www.imdb.com/title/tt0343660/",
            "plot": "Henry Roth is a veterinarian living in Hawaii who falls for Lucy Whitmore, an art teacher. However, after discovering Lucy suffers from short-term memory loss that resets her memory every night, Henry must win her heart anew every single morning.",
            "actors": "Adam Sandler, Drew Barrymore, Rob Schneider, Sean Astin",
            "runtime": "99 min",
            "rated": "PG-13",
            "awards": "Won 1 People's Choice Award. 6 wins & 10 nominations",
            "metascore": "48",
            "imdb_votes": "390,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "17KJk3ErIx0",
            "clip_url": "https://www.youtube-nocookie.com/embed/17KJk3ErIx0",
            "clip_title": "Official Trailer: 50 First Dates (2004)",
            "clip_duration": "2:22",
            "sound_theme": "Tropical Ukulele Strumming & Reggae Acoustic Beats"
    },
    {
            "id": "m_100",
            "title": "13 Going on 30",
            "year": 2004,
            "genres": [
                    "Comedy",
                    "Fantasy",
                    "Romance"
            ],
            "director": "Gary Winick",
            "rating": 6.3,
            "match_keywords": [
                    "time jump",
                    "magazine",
                    "childhood friend",
                    "Manhattan"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNDk0NjYxMzIzOF5BMl5BanBnXkFtZTcwMTc5MzcyMQ@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Thriller group dance routine at magazine party",
                    "emotional": "🌹 Dollhouse wish dust on childhood porch swing"
            },
            "imdb_id": "tt0337563",
            "imdb_url": "https://www.imdb.com/title/tt0337563/",
            "plot": "A 13-year-old girl makes a wish on her birthday and is miraculously transported into her future 30-year-old life as a successful fashion magazine editor in New York City, only to discover she misses her childhood best friend Matt.",
            "actors": "Jennifer Garner, Mark Ruffalo, Judy Greer, Andy Serkis",
            "runtime": "98 min",
            "rated": "PG-13",
            "awards": "Nominated for 4 Teen Choice Awards. 6 nominations total",
            "metascore": "57",
            "imdb_votes": "210,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "_pmFp2W65Fs",
            "clip_url": "https://www.youtube-nocookie.com/embed/_pmFp2W65Fs",
            "clip_title": "13 GOING ON 30 [2004] – Official Trailer (HD)",
            "clip_duration": "2:16",
            "sound_theme": "80s Pop Synth Nostalgia & Sweet Piano Melodies"
    },
    {
            "id": "m_101",
            "title": "Bridget Jones's Diary",
            "year": 2001,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Sharon Maguire",
            "rating": 6.8,
            "match_keywords": [
                    "London",
                    "diary",
                    "awkward romance",
                    "Christmas"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BYmZmZTI2N2MtNDU3Zi00N2YxLWIzMDUtZjU3Y2Y5YWYwOGE5XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Snowy London street run in leopard print underwear",
                    "emotional": "🌹 Blue string soup dinner party with friends"
            },
            "imdb_id": "tt0243155",
            "imdb_url": "https://www.imdb.com/title/tt0243155/",
            "plot": "Bridget Jones is an average 30-something British woman determined to improve herself and find love while writing everything down in a personal diary. She finds herself torn between a charming boss and a quiet barrister in an ugly Christmas jumper.",
            "actors": "Renée Zellweger, Colin Firth, Hugh Grant, Jim Broadbent",
            "runtime": "97 min",
            "rated": "R",
            "awards": "Nominated for 1 Oscar. 8 wins & 29 nominations",
            "metascore": "66",
            "imdb_votes": "260,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "xjlKnDWZYzc",
            "clip_url": "https://www.youtube-nocookie.com/embed/xjlKnDWZYzc",
            "clip_title": "BRIDGET JONES'S DIARY (2001) | Official Trailer | 4K Restoration",
            "clip_duration": "2:20",
            "sound_theme": "Patrick Doyle Orchestral British Pop & Chaka Khan Funk"
    },
    {
            "id": "m_102",
            "title": "To All the Boys I've Loved Before",
            "year": 2018,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Susan Johnson",
            "rating": 7.0,
            "match_keywords": [
                    "love letters",
                    "high school",
                    "fake relationship",
                    "family"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMjA5OTg3Njg2OF5BMl5BanBnXkFtZTgwMjc4MTExNjM@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Ski trip hot tub conversation in winter twilight",
                    "emotional": "🌹 Vintage Diner milkshake contract signing scene"
            },
            "imdb_id": "tt3846674",
            "imdb_url": "https://www.imdb.com/title/tt3846674/",
            "plot": "Lara Jean's quiet high school life is turned upside down when the secret love letters she wrote to every boy she ever had a crush on are mysteriously mailed out to them all, leading to a fake relationship with lacrosse player Peter Kavinsky.",
            "actors": "Lana Condor, Noah Centineo, Janel Parrish, Anna Cathcart",
            "runtime": "99 min",
            "rated": "TV-14",
            "awards": "Won 1 MTV Movie Award. 4 wins & 6 nominations",
            "metascore": "64",
            "imdb_votes": "125,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "555oiY9RWM4",
            "clip_url": "https://www.youtube-nocookie.com/embed/555oiY9RWM4",
            "clip_title": "To All The Boys I've Loved Before | Official Trailer | Netflix",
            "clip_duration": "2:25",
            "sound_theme": "Dreamy Indie Pop & Shimmering Pastel Synths"
    },
    {
            "id": "m_103",
            "title": "The Big Sick",
            "year": 2017,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Michael Showalter",
            "rating": 7.5,
            "match_keywords": [
                    "standup comedy",
                    "culture clash",
                    "hospital",
                    "family"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BYzJkYzg2OTktNzkzMi00MGMzLTljMmEtMjc0NDM3NmUzZWM2XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Standup comedy club dressing room conversation",
                    "emotional": "🌹 Hospital waiting room cross-cultural bond"
            },
            "imdb_id": "tt5462602",
            "imdb_url": "https://www.imdb.com/title/tt5462602/",
            "plot": "Pakistan-born comedian Kumail and grad student Emily fall in love but struggle as their cultures clash. When Emily contracts a mysterious illness, Kumail finds himself forced to navigate the medical crisis with her eccentric parents.",
            "actors": "Kumail Nanjiani, Zoe Kazan, Holly Hunter, Ray Romano",
            "runtime": "120 min",
            "rated": "R",
            "awards": "Nominated for 1 Oscar. 20 wins & 94 nominations",
            "metascore": "86",
            "imdb_votes": "145,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "PJmpSMRQhhs",
            "clip_url": "https://www.youtube-nocookie.com/embed/PJmpSMRQhhs",
            "clip_title": "The Big Sick – Official US Trailer | Amazon Studios",
            "clip_duration": "2:24",
            "sound_theme": "Gentle Acoustic Indie Guitar & Warm Chicago Strings"
    },
    {
            "id": "m_104",
            "title": "Sing Street",
            "year": 2016,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Music",
                    "Romance"
            ],
            "director": "John Carney",
            "rating": 7.9,
            "match_keywords": [
                    "80s music",
                    "Dublin",
                    "school band",
                    "dreams"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMjM4OTExNDkzN15BMl5BanBnXkFtZTgwOTEwMTk2NzE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Drive It Like You Stole It 50s prom hallucination",
                    "emotional": "🌹 Dublin harbor speedboat escape into open sea"
            },
            "imdb_id": "tt3544112",
            "imdb_url": "https://www.imdb.com/title/tt3544112/",
            "plot": "A boy growing up in Dublin during the 1980s escapes his strained family life by starting a band with his schoolmates to impress the mysterious and cool girl he likes, shooting homemade music videos along the way.",
            "actors": "Ferdia Walsh-Peelo, Lucy Boynton, Jack Reynor, Mark McKenna",
            "runtime": "106 min",
            "rated": "PG-13",
            "awards": "Nominated for 1 Golden Globe. 15 wins & 45 nominations",
            "metascore": "79",
            "imdb_votes": "105,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "jYk2Vx1z6lk",
            "clip_url": "https://www.youtube-nocookie.com/embed/jYk2Vx1z6lk",
            "clip_title": "Sing Street Official Trailer #1 (2016) - Aidan Gillen, Maria Doyle Kennedy Movie HD",
            "clip_duration": "2:26",
            "sound_theme": "80s New Wave Pop Rock & Infectious Electric Guitar"
    },
    {
            "id": "m_105",
            "title": "Begin Again",
            "year": 2013,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Music",
                    "Romance"
            ],
            "director": "John Carney",
            "rating": 7.4,
            "match_keywords": [
                    "NYC",
                    "music producer",
                    "rooftop",
                    "songwriting"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNTg0NTA5MDk4MF5BMl5BanBnXkFtZTgwNTU5NTE5MTE@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Underground subway station recording session",
                    "emotional": "🌹 Times Square headphone splitter night promenade"
            },
            "imdb_id": "tt1980929",
            "imdb_url": "https://www.imdb.com/title/tt1980929/",
            "plot": "A chance encounter between a disgraced music-business executive and a young English singer-songwriter new to Manhattan turns into a promising collaboration as they record a full album across the public locations of New York City.",
            "actors": "Keira Knightley, Mark Ruffalo, Adam Levine, Hailee Steinfeld",
            "runtime": "104 min",
            "rated": "R",
            "awards": "Nominated for 1 Oscar. 3 wins & 7 nominations",
            "metascore": "62",
            "imdb_votes": "175,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "uTRCxOE7Xzc",
            "clip_url": "https://www.youtube-nocookie.com/embed/uTRCxOE7Xzc",
            "clip_title": "Begin Again Official Trailer #1 (2014) - Keira Knightley, Adam Levine Movie HD",
            "clip_duration": "2:27",
            "sound_theme": "Lost Stars Acoustic Guitar & NYC Street Sounds"
    },
    {
            "id": "m_106",
            "title": "My Best Friend's Wedding",
            "year": 1997,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "P.J. Hogan",
            "rating": 6.4,
            "match_keywords": [
                    "wedding",
                    "best friends",
                    "Chicago",
                    "jealousy"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BZGQ1NDFkYzAtZDRhNS00NmY2LWI1YzktZjQ4Njk5ZTEwY2FlXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Seafood restaurant Say A Little Prayer singalong",
                    "emotional": "🌹 Chicago riverboat slow dance confession"
            },
            "imdb_id": "tt0119738",
            "imdb_url": "https://www.imdb.com/title/tt0119738/",
            "plot": "When a woman's long-time friend reveals he's engaged, she realizes she has loved him all along and sets out to win him back with only days before the wedding, teaming up with her gay editor friend in Chicago.",
            "actors": "Julia Roberts, Dermot Mulroney, Cameron Diaz, Rupert Everett",
            "runtime": "105 min",
            "rated": "PG-13",
            "awards": "Nominated for 1 Oscar. 8 wins & 17 nominations",
            "metascore": "50",
            "imdb_votes": "150,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "7gRQFgdtAXs",
            "clip_url": "https://www.youtube-nocookie.com/embed/7gRQFgdtAXs",
            "clip_title": "MY BEST FRIEND'S WEDDING [1997] - Official Trailer (HD)",
            "clip_duration": "2:18",
            "sound_theme": "Burt Bacharach Soul Pop & Upbeat Jazz Piano"
    },
    {
            "id": "m_107",
            "title": "Sleepless in Seattle",
            "year": 1993,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Nora Ephron",
            "rating": 6.8,
            "match_keywords": [
                    "Empire State",
                    "radio",
                    "Seattle",
                    "destiny"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNTIxMDI0MTctYTFlMS00YzcyLWI2YjMtNDRhNDRhOGM2YzU2XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Empire State Building Valentine's observation deck",
                    "emotional": "🌹 Seattle houseboat evening radio monologue"
            },
            "imdb_id": "tt0108160",
            "imdb_url": "https://www.imdb.com/title/tt0108160/",
            "plot": "A recently widowed man's son calls a nationwide radio talk show in an attempt to find his father a new partner, capturing the heart of an engaged Baltimore journalist who believes in destiny.",
            "actors": "Tom Hanks, Meg Ryan, Ross Malinger, Bill Pullman",
            "runtime": "105 min",
            "rated": "PG",
            "awards": "Nominated for 2 Oscars. 4 wins & 17 nominations",
            "metascore": "72",
            "imdb_votes": "195,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "ahI9LaOGYcE",
            "clip_url": "https://www.youtube-nocookie.com/embed/ahI9LaOGYcE",
            "clip_title": "Sleepless in Seattle (1993) Trailer #1 | Movieclips Classic Trailers",
            "clip_duration": "2:15",
            "sound_theme": "Classic Big Band Ballads & Romantic Strings"
    },
    {
            "id": "m_108",
            "title": "You've Got Mail",
            "year": 1998,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Nora Ephron",
            "rating": 6.7,
            "match_keywords": [
                    "email",
                    "bookstore",
                    "Upper West Side",
                    "enemies to lovers"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BOGY5NWFlYTAtYmRhMS00NGUzLTlmZjQtMmEzZTEwYTZiOGRhXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Riverside Park springtime flower garden reveal",
                    "emotional": "🌹 Charming Corner Bookstore Christmas window"
            },
            "imdb_id": "tt0128853",
            "imdb_url": "https://www.imdb.com/title/tt0128853/",
            "plot": "Book superstore magnate Joe Fox and independent children's bookstore owner Kathleen Kelly despise each other in person, unaware that they are conducting an anonymous romantic correspondence over 1990s email.",
            "actors": "Tom Hanks, Meg Ryan, Greg Kinnear, Parker Posey",
            "runtime": "119 min",
            "rated": "PG",
            "awards": "Nominated for 1 Golden Globe. 4 wins & 7 nominations",
            "metascore": "57",
            "imdb_votes": "230,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "bjP4s7UUnK8",
            "clip_url": "https://www.youtube-nocookie.com/embed/bjP4s7UUnK8",
            "clip_title": "You've Got Mail (1998) Official Trailer - Tom Hanks, Meg Ryan Movie HD",
            "clip_duration": "2:21",
            "sound_theme": "Acoustic Folk Pop & 90s Dial-Up Dial Tone Nostalgia"
    },
    {
            "id": "m_109",
            "title": "Groundhog Day",
            "year": 1993,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Fantasy",
                    "Romance"
            ],
            "director": "Harold Ramis",
            "rating": 8.0,
            "match_keywords": [
                    "time loop",
                    "weather",
                    "redemption",
                    "Pennsylvania"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMmM3OTlmNWUtODQzNi00YTU4LWExMmQtMDQ1MmU1YTA4ZjhhXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Rachmaninoff piano solo recital at town celebration",
                    "emotional": "🌹 Snow sculpture portrait in moonlit park"
            },
            "imdb_id": "tt0107048",
            "imdb_url": "https://www.imdb.com/title/tt0107048/",
            "plot": "A narcissistic TV weatherman finds himself inexplicably living the same day over and over again in Punxsutawney, Pennsylvania, until he uses his infinite time to better himself and win the heart of his producer.",
            "actors": "Bill Murray, Andie MacDowell, Chris Elliott, Stephen Tobolowsky",
            "runtime": "101 min",
            "rated": "PG",
            "awards": "Won 1 BAFTA Film Award. 7 wins & 17 nominations",
            "metascore": "72",
            "imdb_votes": "690,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "GncQtURdcE4",
            "clip_url": "https://www.youtube-nocookie.com/embed/GncQtURdcE4",
            "clip_title": "Groundhog Day (1993) Trailer #1 | Movieclips Classic Trailers",
            "clip_duration": "2:32",
            "sound_theme": "I Got You Babe Sonny & Cher & Classical Piano"
    },
    {
            "id": "m_110",
            "title": "Hitch",
            "year": 2005,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Andy Tennant",
            "rating": 6.6,
            "match_keywords": [
                    "date doctor",
                    "Manhattan",
                    "advice",
                    "gossip columnist"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNzQ0NjcwNjA5OV5BMl5BanBnXkFtZTcwMTgwNDcyMQ@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Ellis Island jet ski date accident in harbor",
                    "emotional": "🌹 Cooking dinner with swollen allergic reaction face"
            },
            "imdb_id": "tt0386588",
            "imdb_url": "https://www.imdb.com/title/tt0386588/",
            "plot": "A professional 'date doctor' who helps insecure men woo the women of their dreams finds that his time-tested romantic formulas don't work when he falls head over heels for a cynical tabloid columnist.",
            "actors": "Will Smith, Eva Mendes, Kevin James, Amber Valletta",
            "runtime": "118 min",
            "rated": "PG-13",
            "awards": "Won 1 People's Choice Award. 4 wins & 18 nominations",
            "metascore": "58",
            "imdb_votes": "330,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "dMaq_pfxs-0",
            "clip_url": "https://www.youtube-nocookie.com/embed/dMaq_pfxs-0",
            "clip_title": "Hitch (2005) - Trailer",
            "clip_duration": "2:20",
            "sound_theme": "Smooth Urban Soul Grooves & Funky Brass Stabs"
    },
    {
            "id": "m_111",
            "title": "Friends with Benefits",
            "year": 2011,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Will Gluck",
            "rating": 6.5,
            "match_keywords": [
                    "casual dating",
                    "NYC",
                    "headhunter",
                    "Grand Central"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMTQ4NTQ5MTQ1NF5BMl5BanBnXkFtZTcwNTAwNDkyNQ@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Grand Central Terminal flash mob dance serenade",
                    "emotional": "🌹 Hollywood sign rooftop midnight conversation"
            },
            "imdb_id": "tt1632708",
            "imdb_url": "https://www.imdb.com/title/tt1632708/",
            "plot": "A young NYC headhunter convinces a potential recruit from LA to accept a job in New York. They quickly become friends, but things get complicated when they decide to add casual romance to their relationship.",
            "actors": "Justin Timberlake, Mila Kunis, Patricia Clarkson, Woody Harrelson",
            "runtime": "109 min",
            "rated": "R",
            "awards": "Nominated for 2 People's Choice Awards. 4 nominations total",
            "metascore": "63",
            "imdb_votes": "375,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "MxfaGMuiniI",
            "clip_url": "https://www.youtube-nocookie.com/embed/MxfaGMuiniI",
            "clip_title": "Official FRIENDS WITH BENEFITS Trailer - In Theaters 7/22",
            "clip_duration": "2:24",
            "sound_theme": "Upbeat Modern Pop & Indie Hip-Hop Funk"
    },
    {
            "id": "m_112",
            "title": "Legally Blonde",
            "year": 2001,
            "genres": [
                    "Comedy",
                    "Romance"
            ],
            "director": "Robert Luketic",
            "rating": 6.4,
            "match_keywords": [
                    "Harvard Law",
                    "pink",
                    "makeover",
                    "courtroom"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNTEyNjUwMTkxMV5BMl5BanBnXkFtZTcwNjk0NDk0MQ@@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Harvard Law courtroom perm chemistry breakthrough",
                    "emotional": "🌹 Delta Nu sorority bend-and-snap beauty salon"
            },
            "imdb_id": "tt0250494",
            "imdb_url": "https://www.imdb.com/title/tt0250494/",
            "plot": "Elle Woods, a fashionable sorority queen, gets dumped by her boyfriend who attends Harvard Law. She resolves to get admitted to Harvard Law herself to win him back, discovering her natural talent for justice along the way.",
            "actors": "Reese Witherspoon, Luke Wilson, Selma Blair, Matthew Davis",
            "runtime": "96 min",
            "rated": "PG-13",
            "awards": "Nominated for 2 Golden Globes. 8 wins & 13 nominations",
            "metascore": "59",
            "imdb_votes": "240,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "vWOHwI_FgAo",
            "clip_url": "https://www.youtube-nocookie.com/embed/vWOHwI_FgAo",
            "clip_title": "Legally Blonde (2001) | Official Trailer | MGM Studios",
            "clip_duration": "2:15",
            "sound_theme": "High-Energy 2000s Pop & Sassy Brass Horns"
    },
    {
            "id": "m_113",
            "title": "The Wedding Singer",
            "year": 1998,
            "genres": [
                    "Comedy",
                    "Music",
                    "Romance"
            ],
            "director": "Frank Coraci",
            "rating": 6.9,
            "match_keywords": [
                    "80s wedding",
                    "airplane serenade",
                    "heartbreak",
                    "retro"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BYzA1YjM4OTAtN2MzYS00YjBhLTljZGEtMzVlZTg2YzQzY2VkXkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 First-class airplane Grow Old With You serenade",
                    "emotional": "🌹 Wedding reception Love Stinks rock breakdown"
            },
            "imdb_id": "tt0120888",
            "imdb_url": "https://www.imdb.com/title/tt0120888/",
            "plot": "Robbie, a singer, and Julia, a waitress, are both engaged to the wrong people in 1985. Fortune intervenes to help them discover each other, culminating in an iconic first-class airplane musical proposal.",
            "actors": "Adam Sandler, Drew Barrymore, Christine Taylor, Allen Covert",
            "runtime": "97 min",
            "rated": "PG-13",
            "awards": "Won 1 MTV Movie Award. 3 wins & 7 nominations",
            "metascore": "59",
            "imdb_votes": "160,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "Yy-TwYB1UQw",
            "clip_url": "https://www.youtube-nocookie.com/embed/Yy-TwYB1UQw",
            "clip_title": "The Wedding Singer (1998) Trailer #1 | Movieclips Classic Trailers",
            "clip_duration": "2:18",
            "sound_theme": "80s Synthpop Classics & Acoustic Love Ballads"
    },
    {
            "id": "m_114",
            "title": "Letters to Juliet",
            "year": 2010,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Gary Winick",
            "rating": 6.5,
            "match_keywords": [
                    "Verona",
                    "Italy",
                    "love letters",
                    "vineyard"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BMjExNjRjODgtOTVhYi00MDc3LTgyMDktYTBhM2Y1MDVmMmU2XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Verona courtyard Juliet letter extraction",
                    "emotional": "🌹 Tuscan vineyard golden hour sunset proposal"
            },
            "imdb_id": "tt0892318",
            "imdb_url": "https://www.imdb.com/title/tt0892318/",
            "plot": "Sophie dreams of becoming a writer and travels to Verona, Italy, where she meets the 'Secretaries of Juliet' who answer love letters. She finds a 50-year-old unanswered letter and inspires its author to search for her long-lost true love.",
            "actors": "Amanda Seyfried, Gael García Bernal, Vanessa Redgrave, Christopher Egan",
            "runtime": "105 min",
            "rated": "PG",
            "awards": "Won 1 Golden Trailer Award. 3 nominations total",
            "metascore": "47",
            "imdb_votes": "115,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "8j0qMY-LeKM",
            "clip_url": "https://www.youtube-nocookie.com/embed/8j0qMY-LeKM",
            "clip_title": "Letters To Juliet (2010) Official Trailer - Amanda Seyfried, Gael García Bernal Movie HD",
            "clip_duration": "2:20",
            "sound_theme": "Italian Mandolin Serenades & Sun-Drenched Acoustic Guitars"
    },
    {
            "id": "m_115",
            "title": "Rye Lane",
            "year": 2023,
            "genres": [
                    "Comedy",
                    "Drama",
                    "Romance"
            ],
            "director": "Raine Allen-Miller",
            "rating": 7.2,
            "match_keywords": [
                    "South London",
                    "art",
                    "walk and talk",
                    "modern love"
            ],
            "poster_url": "https://m.media-amazon.com/images/M/MV5BZDY0M2ExZTUtM2QzMy00ZmI1LWI2ZTgtMjAwMzkxNDAwYTU5XkEyXkFqcGc@._V1_QL75_UX380_CR0,0,380,562_.jpg",
            "poster_variants": {
                    "action": "💖 Peckham colorful market stroll with ice cream",
                    "emotional": "🌹 Art gallery restroom accidental meet-cute"
            },
            "imdb_id": "tt15894294",
            "imdb_url": "https://www.imdb.com/title/tt15894294/",
            "plot": "Two twenty-somethings, both reeling from bad break-ups, connect over the course of an eventful day in South London, helping each other deal with their respective exes and potentially restoring their faith in romance.",
            "actors": "Vivian Oparah, David Jonsson, Poppy Allen-Quarmby",
            "runtime": "82 min",
            "rated": "R",
            "awards": "Won 1 BAFTA Award. 10 wins & 37 nominations",
            "metascore": "83",
            "imdb_votes": "35,000",
            "media_type": "movie",
            "total_seasons": "Feature Film",
            "trailer_id": "SqcF_GI3mOA",
            "clip_url": "https://www.youtube-nocookie.com/embed/SqcF_GI3mOA",
            "clip_title": "RYE LANE | Official Trailer | Searchlight Pictures",
            "clip_duration": "2:15",
            "sound_theme": "Kwes Vibrant South London Hip-Hop & Soul Chords"
    }
]

USER_PROFILES = {
    "u_romcom_fan": {
        "name": "Emma — Rom-Coms, Feel-Good & TV Dramedies",
        "preferred_genres": ["Romance", "Comedy", "Feel-Good"],
        "watch_history": ["Fleabag", "Friends", "Ted Lasso", "Crazy Rich Asians", "About Time", "Palm Springs", "La La Land"],
        "taste_vector": [0.10, 0.10, 0.10, 0.98, 0.92, 0.65, 0.35, 0.05],
        "artwork_bias": "emotional"
    },
    "u_scifi_fan": {
        "name": "Alex Chen — Sci-Fi, Cyberpunk & Mind-Benders",
        "preferred_genres": ["Sci-Fi", "Mystery", "Action"],
        "watch_history": ["Dark", "Severance", "Black Mirror", "Interstellar", "Blade Runner 2049", "The Matrix", "Dune: Part Two"],
        "taste_vector": [0.98, 0.85, 0.75, 0.15, 0.20, 0.50, 0.30, 0.20],
        "artwork_bias": "action"
    },
    "u_drama_cinephile": {
        "name": "Sarah Miller — Auteur Cinema, Crime & Peak TV Drama",
        "preferred_genres": ["Drama", "Crime", "Biography"],
        "watch_history": ["Peaky Blinders", "Succession", "Better Call Saul", "Chernobyl", "The Godfather", "Oppenheimer", "The Shawshank Redemption"],
        "taste_vector": [0.35, 0.30, 0.95, 0.25, 0.30, 0.98, 0.20, 0.30],
        "artwork_bias": "emotional"
    },
    "u_family_animation": {
        "name": "Maya — Animation, Anime & Epic Worldbuilding",
        "preferred_genres": ["Animation", "Adventure", "Fantasy", "Action"],
        "watch_history": ["Arcane", "Attack on Titan", "Death Note", "Spirited Away", "Spider-Man: Across the Spider-Verse", "Your Name."],
        "taste_vector": [0.70, 0.75, 0.35, 0.40, 0.75, 0.40, 0.98, 0.05],
        "artwork_bias": "emotional"
    },
    "u_horror_thriller": {
        "name": "Liam Vance — Psychological Thriller, Mystery & True Crime",
        "preferred_genres": ["Crime", "Mystery", "Thriller", "Horror"],
        "watch_history": ["The Mentalist", "Mindhunter", "True Detective", "Dexter", "Fargo", "Get Out", "The Silence of the Lambs", "Se7en"],
        "taste_vector": [0.40, 0.30, 0.98, 0.05, 0.10, 0.60, 0.10, 0.98],
        "artwork_bias": "action"
    },
    "u_action_blockbuster": {
        "name": "Noah Rivera — High-Octane Action, Heists & Adrenaline",
        "preferred_genres": ["Action", "Crime", "Thriller"],
        "watch_history": ["Money Heist", "Breaking Bad", "The Boys", "Vikings", "The Dark Knight", "Top Gun: Maverick", "John Wick: Chapter 4"],
        "taste_vector": [0.75, 0.98, 0.85, 0.15, 0.40, 0.30, 0.25, 0.20],
        "artwork_bias": "action"
    }
}


def compute_genre_vector(genres: List[str]) -> List[float]:
    """Encodes movie/series genres into 8D embedding vector:
    [SciFi, Action, Thriller/Crime/Mystery, Romance, Comedy, Drama/Bio, Animation/Family, Horror]
    """
    v = [0.05] * 8
    g_lower = [g.lower() for g in genres]
    
    # 0: Sci-Fi & Space
    if any(k in g_lower for k in ["sci-fi", "scifi", "science fiction"]): v[0] = 0.95
    elif any(k in g_lower for k in ["adventure", "fantasy"]): v[0] = max(v[0], 0.65)
    
    # 1: Action & Superhero
    if "action" in g_lower: v[1] = 0.95
    elif "adventure" in g_lower: v[1] = max(v[1], 0.60)
    
    # 2: Thriller, Crime & Mystery
    if any(k in g_lower for k in ["thriller", "crime", "mystery", "neo-noir"]): v[2] = 0.95
    
    # 3: Romance & Love
    if "romance" in g_lower: v[3] = 0.98
    
    # 4: Comedy & Satire
    if "comedy" in g_lower: v[4] = 0.95
    
    # 5: Drama, Biography & History
    if any(k in g_lower for k in ["drama", "biography", "history"]): v[5] = 0.90
    
    # 6: Animation, Anime & Family
    if any(k in g_lower for k in ["animation", "family", "anime"]): v[6] = 0.98
    
    # 7: Horror & Psychological
    if "horror" in g_lower: v[7] = 0.96
    
    return v


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0: return 0.0
    return dot / (norm1 * norm2)


def get_recommendations_for_user(user_key: str, top_k: int = 20) -> Dict[str, Any]:
    user = USER_PROFILES.get(user_key, USER_PROFILES["u_romcom_fan"])
    u_vec = user["taste_vector"]
    
    scored_movies = []
    for m in MOVIES_CATALOG:
        m_vec = compute_genre_vector(m["genres"])
        raw_sim = cosine_similarity(u_vec, m_vec)
        
        is_watched = m["title"] in user["watch_history"]
        
        p_click = min(0.98, max(0.12, raw_sim * 0.95 + random.uniform(-0.015, 0.015)))
        p_complete = min(0.96, max(0.20, (float(m["rating"]) / 10.0) * 0.65 + raw_sim * 0.35))
        
        score = (p_click * 0.52) + (p_complete * 0.48)
        if is_watched:
            score *= 0.30  # Demote watched titles in personalized feed
            
        selected_poster = m["poster_variants"].get(user["artwork_bias"], m["poster_variants"].get("emotional", list(m["poster_variants"].values())[0]))

        scored_movies.append({
            **m,
            "match_pct": round(raw_sim * 100, 1),
            "p_click": round(p_click, 3),
            "p_complete": round(p_complete, 3),
            "final_score": round(score, 4),
            "is_watched": is_watched,
            "selected_poster": selected_poster,
            "artwork_style": user["artwork_bias"]
        })

    scored_movies.sort(key=lambda x: x["final_score"], reverse=True)

    # Filter Rom-Coms & Feel-Good specifically
    romcoms_only = [m for m in scored_movies if "Romance" in m["genres"] or "Comedy" in m["genres"]]
    
    # Filter Top Series specifically
    series_only = [m for m in scored_movies if m.get("media_type") == "series"]

    return {
        "user_profile": user,
        "recommendations": scored_movies[:top_k],
        "romcoms": romcoms_only[:24],
        "top_series": series_only[:16],
        "all_scored": scored_movies,
        "total_catalog_count": len(MOVIES_CATALOG),
        "movies_count": sum(1 for m in MOVIES_CATALOG if m.get("media_type") == "movie"),
        "series_count": sum(1 for m in MOVIES_CATALOG if m.get("media_type") == "series")
    }
