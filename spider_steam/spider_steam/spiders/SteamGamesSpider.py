import scrapy
from .. import items


COOKIES = {
    'birthtime': 1038690001,
    'lastagecheckage': '1-0-2003',
}


def delete_tabs(string: str) -> str:
    return string.replace('\n', '').replace('\r', '').replace('\t', '')


class SteamGamesSpider(scrapy.Spider):
    name = 'SteamGamesSpider'
    allowed_domains = ['store.steampowered.com']
    start_urls = [
        f'https://store.steampowered.com/search/?term={search}&page={p}'
        for search in ['Horror', 'Anime', 'Two players']
        for p in map(str, range(1, 3))
    ]

    def parse(self, response):
        hrefs = response.xpath('//div[@id="search_resultsRows"]/a/@href').extract()
        for href in hrefs:
            a = href.replace('/agecheck', '')
            if 'bundle' in href:
                yield scrapy.Request(url=href, callback=self.parse_bundle, cookies=COOKIES)
            else:
                yield scrapy.Request(url=href, callback=self.parse_game, cookies=COOKIES)


    def parse_game(self, response):
        item = items.Game()
        name = response.xpath('//div[@id="appHubAppName"]/text()').extract()
        category = response.xpath('//div[@class="blockbg"]/a/text()').extract()
        review = response.xpath('//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').extract()
        created_at = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').extract()
        developer_distributor = response.xpath('//div[@class="dev_row"]/div/a/text()').extract()
        tags = response.xpath('//div[@class="glance_tags_ctn popular_tags_ctn"]//a/text()').extract()
        cost = response.xpath('//div[@class="game_purchase_price price"]/text()').extract_first()
        if cost:
            cost_with_discount = response.xpath('//div[@class="game_purchase_price price"]/text()').extract_first()
        else:
            cost = response.xpath('//div[@class="discount_original_price"]/text()').extract_first()
            cost_with_discount = response.xpath('//div[@class="discount_final_price"]/text()').extract_first()
        platforms = response.xpath('//div[@class="game_area_purchase_platform"]/span/@class').extract()
        if not platforms:
            platforms = ['Is unknown']

        item['name'] = ' '.join(name).strip()
        item['category'] = ' -> '.join(category[1:]).strip()
        if review:
            item['review_count'] = review[-1].split()[4].strip()
            item['review_grade'] = review[-1].split()[1].strip()
        else:
            item['review_count'] = '0'
            item['review_grade'] = 'N/A'
        item['created_at'] = ' '.join(created_at).strip()
        item['developer'] = developer_distributor[0].strip()
        item['distributor'] = developer_distributor[1].strip()
        item['tags'] = delete_tabs(', '.join(tags)).strip()
        if cost:
            item['cost'] = cost.replace('уб', '').strip()
            item['cost_with_discount'] = cost_with_discount.replace('уб', '').strip()
        else:
            item['cost'] = 'Is unknown'.strip()
            item['cost_with_discount'] = 'Is unknown'.strip()
        item['platforms'] = ', '.join(set(platforms)).replace('platform_img ', '').strip()
        yield item

    def parse_bundle(self, response):
        hrefs = response.xpath('//div[@class="bundle_package_item complete_the_set"]//a/@href').extract()
        for href in hrefs:
            yield scrapy.Request(url=href, callback=self.parse_game, cookies=COOKIES)
