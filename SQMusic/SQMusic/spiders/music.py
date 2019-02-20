import scrapy
from ..items import SqmusicItem, SQmusicItem


class SQMusic(scrapy.Spider):
    name = 'SQMusic'
    cate = [1] * 7 + [2] * 7 + [3] * 2 + [4] * 4 + [5]
    page = list(range(1, 8)) + list(range(1, 8)) + list(range(1, 3)) + list(range(1, 5)) + [1]
    start_urls = ['https://www.sq688.com/singer/1000{}/{}.html'.format(x[0], x[1]) for x in zip(cate, page)]

    def parse(self, response):

        music_links = response.xpath('/html/body/div[2]/ul[2]/li/a/@href').extract()
        singer = response.xpath('/html/body/div[2]/ul[2]/li/a/h5/text()').extract()
        picture = response.xpath('/html/body/div[2]/ul[2]/li/a/img/@data-original').extract()
        category = response.url.split('/')[-2][-1]
        item = SqmusicItem()
        for x in zip(singer, picture):
            item['name'] = x
            item['category'] = category
            yield item
        for music_link in music_links:
            yield scrapy.Request('https://www.sq688.com{}'.format(music_link), callback=self.music_parse)

    def music_parse(self, response):

        links = response.xpath('//*[@class="dw"]/@href').extract()
        for link in links:
            yield scrapy.Request('https://www.sq688.com{}'.format(link), callback=self.dw_parse)

    def dw_parse(self, response):

        music_name = response.xpath('//*[@class="dcenter"][1]/div[1]/h2/text()').extract()[0].strip()
        size = response.xpath('//*[@class="dcenter"][1]/div[1]/p[2]/text()').extract()[0]
        singer = response.xpath('//*[@class="dcenter"][1]/div[1]/p[1]/a/text()').extract()[0]
        link = response.xpath('//*[@class="dcenter"][1]/div[2]/p/text()').extract()[0]
        item = SQmusicItem()
        infos = []
        infos.append(singer)
        infos.append(music_name)
        infos.append(size)
        infos.append(link)
        item['infos'] = infos
        yield item


# if __name__ == '__main':
#     from scrapy.crawler import CrawlerProcess
#     process = CrawlerProcess()
#     process.crawl(SQMusic)
#     process.start()