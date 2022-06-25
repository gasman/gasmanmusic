import datetime
import re

from django.core.management.base import BaseCommand
from home.models import News

NEWS_ITEMS = [
    """18 Dec 2019 - Created the music for <a href="https://lexaloffle.com/bbs/?pid=71186">Katamari Christmassy</a>, p01's Pico-8 tribute to Katamari Damacy for #pico8advent""",
    """7 Dec 2019 - Participated in the YM Rockerz musicdisk <a href="https://www.youtube.com/watch?v=usdCLuJtXMI">Faker Bashing</a>, released at Silly Venture 2019, with a new track <i>To The Ends Of The Earth</i>""",
    """17 Aug 2019 - Released <a href="https://www.youtube.com/watch?v=Xxfv1D_sopM">New School Reunion</a> at <a href="https://2019.evoke.eu/">Evoke 2019</a>, Cologne, DE - a Pico-8 demo in collaboration with Rift, with code by Mantratronic and Gasman, and music by Gasman""",
    """13 July 2019 - New track <a href="https://demozoo.org/music/206171/">Dance All Night</a> released at <a href="https://www.lostparty.pl/2019/">Lost Party 2019</a>, Licheń Stary, PL""",
    """1 June 2019 - Released <a href="https://www.youtube.com/watch?v=_p3asKU9YIU">Carcharodon Minor</a> at <a href="http://outlinedemoparty.nl/">Outline 2019</a>, Willemsoord, NL - Baby Shark but it's coded in 128 bytes on the ZX Spectrum...""",
    """21 April 2019 - Two Spectrum releases at <a href="https://2019.revision-party.net/">Revision 2019</a>, Saarbrücken, DE - <a href="https://www.youtube.com/watch?v=DgNGVoQcN-Y">The Brexecutable Music Compo Is Over</a>, an anti-Brexit message to the European demoscene, and <a href="https://www.youtube.com/watch?v=mgXRXDfQ0xw">Megademica</a>, an epic 8-minute 4K megademo coded by SerzhSoft with music by Gasman""",
    """16 March 2019 - New track <a href="https://demozoo.org/music/201077/">Tim Will Rock You</a> released at <a href="http://forever8.net/">Forever 2019</a>, Horná Súča, SK - a combined tribute to Tim Follin and Queen""",
    """16 Feb 2019 - Live set at <a href="https://hackerhotel.nl/">Hackerhotel 2019</a>, Garderen, NL""",
    """28 Dec 2018 - Created the <a href="https://twitter.com/gasmanic/status/1079164419488268288">QR code easter egg and playable Nohzdyve game</a> for <i>Black Mirror: Bandersnatch</i>!""",
    """8 Dec 2018 - Live set at <a href="https://www.facebook.com/events/340019166565812/">Until It Bleeps</a>, London, UK""",
    """7 Nov 2018 - <a href="http://www.retroaccion.org/retroconciertazo-rocknmidi">Live set at RetroMañía 2018</a>, Zaragoza, ES""",
    """20 Oct 2018 - New track <a href="https://demozoo.org/music/194800/">Dynamite (ninja versus pyrotechnic)</a> released at <a href="http://trsac.dk/">TRSAC 2018</a>, Århus, DK""",
    """2 Sept 2018 - Live set at <a href="https://www.emfcamp.org/">Electromagnetic Field</a>, Eastnor, UK, and the unveiling of <a href="http://gasman.zxdemo.org/speczilla/">a giant working foam ZX Spectrum</a>...""",
    """20 June 2018 - Released <a href="https://demozoo.org/productions/188679/">Buttercream Sputnik</a> at <a href="http://www.novaparty.org/">NOVA 2018</a>, Budleigh Salterton, UK - a Spectrum demo featuring a new graphics mode and a chiptune cover of <i>Little Fluffy Clouds</i> by The Orb""",
    """31 March 2018 - New track <a href="https://demozoo.org/music/185141/">Cover Story</a> released at <a href="https://2018.revision-party.net/">Revision 2018</a>, Saarbrücken, DE""",
    """5 Aug 2017 - Presentation <a href="https://www.youtube.com/watch?v=7OYoEyU0g4s">Zero to chiptune in one hour</a> at SHA2017, Zeewolde, NL - creating <a href="https://soundcloud.com/matt-westcott/the-archers">a chiptune cover of the theme from <i>The Archers</i></a> live on stage :-)""",
    """23 June 2017 - Live set at <a href="http://www.novaparty.org/">NOVA 2017</a>, Budleigh Salterton, UK""",
    """27 May 2017 - Released <a href="https://www.youtube.com/watch?v=FLz9jf2qtgc">Sandstorm</a> at <a href="http://outlinedemoparty.nl/">Outline 2017</a>, Willemsoord, NL - a ZX Spectrum lyrical take on the Darude dancefloor anthem...""",
    """18 March 2017 - Released <a href="https://www.youtube.com/watch?v=Ca5-ihTeYxw">Ultraviolet</a> at <a href="http://forever8.net/">Forever 2017</a>, Horná Súča, SK - a boundary-pushing ZX Spectrum megademo with an all-new Gasman soundtrack!""",
    """6-7 Aug 2016 - Two live sets at <a href="https://www.emfcamp.org/">Electromagnetic Field</a>, Guildford, UK - solo and head-to-head with <a href="http://2xaa.fm/">2xAA</a>!""",
    """16 July 2016 - Released <a href="https://www.youtube.com/watch?v=EY-cnqIaIkI">In The Future</a> at Sundown demo party, Budleigh Salterton, UK - a song and ZX Spectrum music video about our continuing lack of jetpacks""",
    """6 May 2016 - Live set at <a href="http://outlinedemoparty.nl/">Outline demoparty</a>, Willemsord, NL""",
    """26 March 2016 - Released <a href="https://www.youtube.com/watch?v=D9eduiQPY_c">Harder, Better, Manic, Miner</a> at Revision demo party, Saarbrucken, DE - a ZX Spectrum tribute to Daft Punk and Manic Miner in under 4K of code""",
    """19 March 2016 - New track <a href="https://demozoo.org/music/154614/">Worlds Apart</a> released at Forever demo party, Horná Súča, SK""",
    """10 Sept 2015 - Open stage set at SuperByte Festival, Manchester, UK""",
    """14 Aug 2015 - Concert at Chaos Communication Camp, Zehdenick, DE""",
    """8 Aug 2015 - The new <a href="http://www.zxvega.co.uk">Sinclair ZX Spectrum Vega</a> computer features a new Gasman track <i>Awakening</i> on the game selection menu!""",
    """24 Jul 2015 - Concert at Euskal Encounter, Bilbao, ES - <a href="http://www.retroaccion.org/retroconciertazo-chiptune-wars">videos / photos</a>""",
    """19 Jul 2015 - <a href="http://chipmusic.org/forums/post/232659/#p232659">New track <i>Masterplan</i> released</a>, as part of the WeeklyTreats project""",
    """14 May 2015 - Concert at Outline demoparty, Willemsord, NL - <a href="https://www.youtube.com/watch?v=5hYM0s96Y24">video</a>""",
    """14 March 2015 - <a href="http://www.youtube.com/watch?v=LxPXLIALJJI"><i>The Mahler Project</i></a> released, a documentary about the <i>Geek Out!</i> event - <a href="http://matt.west.co.tt/spectrum/the-mahler-project/">blog</a>""",
    """6 Dec 2014 - <i>Geek Out!</i> retrocomputing event at the Museum of the History of Science, Oxford, UK, featuring Gasman's attempt to solve a 30 year old programming challenge by performing Mahler's First Symphony on 12 networked ZX Spectrums...""",
    """7 Nov 2014 - Concert at Kindergarden demoparty, Haga, NO""",
    """28 Oct 2014 - New album <a href="http://yerzmyey.i-demo.pl/"><i>Chiptunes</i> by Yerzmyey</a> released, featuring the guest track <i>Spacecake</i> by Gasman""",
    """3 Oct 2014 - Concert at Deadline demoparty, Berlin, DE""",
    """29-31 Aug 2014 - Concert and closing set at Electromagnetic Field, Newton Longville, UK - <a href="https://www.youtube.com/watch?v=kTmA445jbeI">video</a>""",
]

class Command(BaseCommand):
    help = 'Creates news records for old news items'

    def handle(self, *args, **options):
        for item_text in NEWS_ITEMS:
            range_match = re.match(r'(\d+)-(\d+) (\w+) (\d+) - (.*)', item_text)
            if range_match:
                start_date_str = "%s %s %s" % (range_match[1], range_match[3][:3], range_match[4])
                end_date_str = "%s %s %s" % (range_match[2], range_match[3][:3], range_match[4])
                start_date = datetime.datetime.strptime(start_date_str, "%d %b %Y")
                end_date = datetime.datetime.strptime(end_date_str, "%d %b %Y")
                body = range_match[5]
            else:
                date_match = re.match(r'(\d+) (\w+) (\d+) - (.*)', item_text)
                start_date_str = "%s %s %s" % (date_match[1], date_match[2][:3], date_match[3])
                start_date = datetime.datetime.strptime(start_date_str, "%d %b %Y")
                end_date = None
                body = date_match[4]

            News.objects.create(
                start_date=start_date, end_date=end_date, body=body
            )
