import json
import scrapy


class TibiaPlayersSpider(scrapy.Spider):
    name = 'tibia_players'
    allowed_domains = ['tibia.com']
    start_urls = ['https://www.tibia.com/community/?subtopic=worlds']
    worlds = [ ]

    def parse(self, response):
        selector = response.css('#worlds > div.Border_2 > div > div > div > table > tr > td > div > table > tr:nth-child(3) > td > div.TableContentAndRightShadow > div > table > tr > td > a')
        yield from self.parse_worlds(selector, response)

    def parse_worlds(self, worlds, response):
        for world in worlds:
            world_url = world.css('a[href]').attrib['href']
            yield scrapy.Request(url = world_url, callback = self.get_players_from_world, meta={'world': world.css('*::text').get()})
    
    def get_players_from_world(self, response):
        players = response.css('#worlds > div.Border_2 > div > div > div:nth-child(5) > table  > tr > td > div > table  > tr:not(:first-child) a[href]::text').getall()
        world = {}
        world['world'] = response.meta.get('world')
        world['players'] = [ player.replace(u'\xa0', u' ') for player in players ]
        self.worlds.append(world)
        
    
    def close(self, reason):
        with open('tibia_players.json', 'w') as f:
            f.write(json.dumps(self.worlds, indent=4))
            f.close()
