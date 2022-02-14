import scrapy
from scrapy import Request


class PmSpider(scrapy.Spider):
    name = 'pm'
    allowed_domains = ['unite.pokemon.com/en-us/pokemon/']
    start_urls = ['https://unite.pokemon.com/en-us/pokemon/']
    
    def parse(self, response):
        
        k = []
        for hreflinks in response.xpath('''//a[@class = 'pokemon-card pokemon-card--roster']/@href'''):
            k.append(hreflinks.get().split('/')[-2])
            
        
        full_link = []
        for names in k:
            full_link.append('https://unite.pokemon.com/en-us/pokemon/' + names + '/')
               
        for url in full_link:
            yield Request(url, callback=self.parse_get_data, dont_filter = True)
    
    
    def parse_get_data(self, response):
        
        Name = response.xpath('''//span[(@class = 'section-title__text')]''')
        Specification = response.xpath('''//div[(@class = 'section-body__children')]''')
        Roles = response.xpath('''//div[(@class = 'pokemon-stats__battle vp-slide vp-slide--right')]''')
        BothRolesData = Roles.xpath('.//text()').extract() #Because div tag had two p tags with pill classes which had the 
                                                           #required Role and Ranged_or_Melee information
        Difficulty = response.xpath('''//div[@class = ('pokemon-stats__difficulty vp-slide vp-slide--right vp-delay-1')]''')
        DifficultyText = Difficulty.xpath('.//text()').get()
        DifficultyTextTemp = DifficultyText.split(': ')
        Stats = response.xpath('''//ul[@class = ('pokemon-stats__list')]/li/span[@class = ('visually-hidden')]''')
        AllStatsData = Stats.xpath('.//text()').extract()
        sa = []
    
        for i in AllStatsData:
            j = i.split(' ')
            sa.append(j[1])
            
        print(sa)
        
        
        
        yield{
            
            'Name' : Name.xpath('.//text()').get(),
            'Description' : Specification.xpath('.//text()').get(),
            'Role' : BothRolesData[0],
            'Ranged_or_Melee' : BothRolesData[1],
            'UsageDifficulty' : DifficultyTextTemp[1],
            'Offense' : sa[0],
            'Endurance' : sa[1],
            'Mobility' : sa[2],
            'Scoring': sa[3],
            'Support' : sa[4]
           }
                  
        pass
