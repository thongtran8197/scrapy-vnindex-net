import json

import scrapy

from ..items import VnBizItem
import time
import re
class VnBizSpider(scrapy.Spider):
    name = "vn_biz"
    start_urls = ["https://data.vietnambiz.vn/goods"]

    custom_settings = {
        "FEED_EXPORT_FIELDS": ["name", "unit"],
        "ITEM_PIPELINES": {"vnindex.pipelines.VnBizDataSpiderPipeline": 1}
    }
    domain_url = "https://api.wichart.vn/vietnambiz/vi-mo?"
    goods_urls = ['lon_hoi_trung_quoc', 'heo_hoi', 'bot_giay', 'vai_coton', 'dau_co_malaysia', 'giay_gon_song_trung_quoc', 'dau_nanh_my', 'duong', 'ca_phe', 'tieu', 'vai_cotton_my', 'gao_tpxk', 'tom_su', 'tom_the', 'lua', 'gao_nguyen_lieu', 'phu_pham_lua_gao', 'quang_sat', 'chi', 'thiec', 'kem', 'nhom', 'dong', 'niken', 'vang', 'bac', 'ure_trung_dong', 'luu_huynh', 'phot_pho', 'xut_naoh_trung_quoc', 'phan_dap_trung_quoc', 'phan_urea_trung_quoc', 'phan_ure', 'thep_day_trung_quoc', 'thep_thanh_trung_quoc', 'x_m', 'thep_phe_anh', 'thep_thanh_anh', 'hrc_trung_quoc', 'da_0_4', 'da_mi_sang', 'da_1x2', 'da_hoc', 'ton_lanh_mau_hoa_sen_045mm', 'ton_lanh_hoa_sen_045mm', 'be_tong_nhua_min', 'nhua_duong_60_70', 'ong_nhua_27x18mm', 'ong_nhua_60x2mm', 'ong_nhua_90x29mm', 'son_lot_khang_kiem_cao_cap', 'son_noi_that_tieu_chuan', 'son_ngoai_that_tieu_chuan', 'kinh_mau_trang', 'kinh_solar', 'day_cap_dien', 'xi_mang_pcb', 'be_tong_mac_300', 'gach_dat_set_nung', 'coc_be_tong_du_ung_luc', 'thep', 'than_coc', 'khi_lpg_trung_quoc', 'dau_wti', 'khi_thien_nhien', 'than_newcastle', 'xang_dau', 'mazut', 'cao_su_nhat_ban', 'pet_trung_quoc', 'nhua_pvc_trung_quoc', 'nhua_pp_trung_quoc', 'cao_su']
    currency_interest_rate_urls = ['ctt', 'hd', 'td', 'dhtg', 'dtnh', 'lslnh', 'lsdh', 'lshd']
    macro_economic_urls = ['gdp', 'gdpbinhquan', 'cpi', 'iip', 'pmi', 'hhdv', 'vdtptxh', 'vdtnsnn', 'fdi', 'cctm', 'cctt', 'vt', 'kqt', 'ds', 'tn', 'ld', 'tcns', 'ncp']

    def start_requests(self):
        for url in self.get_start_urls(c_type="marco"):
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        data = json.loads(response.text).get("chart", {})
        prefix_file_name = self.convert_vietnamese(data.get("name", "")).replace(" ", "_")
        series = data.get("series", [])
        for v in series:
            unit = v.get("unit")
            end_fix_file_name = self.convert_vietnamese(v.get("name", "")).replace(" ", "_")
            file_name = prefix_file_name + "_" + end_fix_file_name
            charts_data = v.get("data", [])
            for chart_data in charts_data:
                data_item = VnBizItem(
                    date=time.strftime('%d-%m-%Y', time.gmtime(chart_data[0]/1000)),
                    unit=unit,
                    value=chart_data[1] if chart_data[1] is not None else "",
                    file_name=file_name,
                )
                yield data_item

    def get_start_urls(self, c_type: str = "good") -> list:
        start_urls = []
        if c_type == "good":
            for v in self.goods_urls:
                start_urls.append(self.domain_url + "key=hang_hoa&" + f"name={v}")
        elif c_type == "rate":
            for v in self.currency_interest_rate_urls:
                start_urls.append(self.domain_url + f"name={v}")
        elif c_type == "marco":
            for v in self.macro_economic_urls:
                start_urls.append(self.domain_url + f"name={v}")
        return start_urls

    def convert_vietnamese(self, text: str) -> str:
        """
        Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
        text: input string to be converted
        Return: string converted
        """
        patterns = {
            '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
            '[đ]': 'd',
            '[èéẻẽẹêềếểễệ]': 'e',
            '[ìíỉĩị]': 'i',
            '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
            '[ùúủũụưừứửữự]': 'u',
            '[ỳýỷỹỵ]': 'y'
        }
        output = text
        for regex, replace in patterns.items():
            output = re.sub(regex, replace, output)
            # deal with upper case
            output = re.sub(regex.upper(), replace.upper(), output)
        return output

