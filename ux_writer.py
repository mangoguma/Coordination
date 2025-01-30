from openai import OpenAI
import json
from abc import ABC, abstractmethod


class SizeChooser(ABC):
    client = None

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    @abstractmethod
    def get_size_info(self, url):
        """Extract size information from the given URL."""
        pass

    def choose_size(self, user_info, size_info, product_url):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 고객에게 가장 적합한 사이즈를 추천하는 패션 전문가입니다.

응답 형식:
추천 사이즈: [사이즈]
설명: [추천 이유 설명]

- 고객 정보와 사이즈 측정값을 분석하여 정확한 사이즈를 추천해주세요
- 추천 사이즈에 대한 이유는 한국어로 작성하고, 최대한 자세히 적어주세요
- 링크에서 상품의 특징과 사람들의 리뷰를 함께 참고해주세요
"""
                },
                {
                    "role": "user",
                    "content": f"""Customer Information:
{user_info}

Product URL:
{product_url}

Size Information:
{json.dumps(size_info, ensure_ascii=False, indent=2)}"""
                },
            ],
        )
        return response.choices[0].message.content
    

class TopSizeChooser(SizeChooser):
    def get_size_info(self, url):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 상의(셔츠, 자켓 등) 상품 페이지에서 사이즈 정보를 추출하는 전문가입니다.
                    주어진 URL에 접속하여 상품 페이지의 실제 사이즈표에서 정보를 추출해주세요.
                    
                    중요:
                    - 예시 데이터가 아닌 실제 URL의 상품 사이즈표 데이터를 추출해야 합니다
                    - 상품 페이지의 사이즈표를 찾아 정확한 측정값을 가져와주세요
                    - 측정값이 없는 경우 "-"를 사용하세요
                    - 제공된 사이즈만 포함하세요
                    - 모든 측정값은 센티미터(cm) 단위입니다
                    
                    다음 JSON 형식으로 응답해주세요:
                    {
                        "sizes": [
                            {
                                "size": "실제사이즈",
                                "measurements": {
                                    "총장": "실제측정값",
                                    "가슴단면": "실제측정값",
                                    "어깨너비": "실제측정값",
                                    "소매길이": "실제측정값"
                                }
                            }
                        ]
                    }"""
                },
                {
                    "role": "user",
                    "content": f"이 URL에서 실제 상품의 사이즈표 정보를 추출해주세요: {url}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        sizes_data = {
            '사이즈': [],
            '총장 (cm)': [],
            '가슴단면 (cm)': [],
            '어깨너비 (cm)': [],
            '소매길이 (cm)': []
        }
        
        for size_info in result['sizes']:
            sizes_data['사이즈'].append(size_info['size'])
            sizes_data['총장 (cm)'].append(size_info['measurements'].get('총장', '-'))
            sizes_data['가슴단면 (cm)'].append(size_info['measurements'].get('가슴단면', '-'))
            sizes_data['어깨너비 (cm)'].append(size_info['measurements'].get('어깨너비', '-'))
            sizes_data['소매길이 (cm)'].append(size_info['measurements'].get('소매길이', '-'))
        
        return sizes_data


class LowerSizeChooser(SizeChooser):
    def get_size_info(self, url):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 하의(바지, 스커트 등) 상품 페이지에서 사이즈 정보를 추출하는 전문가입니다.
                    주어진 URL에 접속하여 상품 페이지의 실제 사이즈표에서 정보를 추출해주세요.
                    
                    중요:
                    - 예시 데이터가 아닌 실제 URL의 상품 사이즈표 데이터를 추출해야 합니다
                    - 상품 페이지의 사이즈표를 찾아 정확한 측정값을 가져와주세요
                    - 측정값이 없는 경우 "-"를 사용하세요
                    - 제공된 사이즈만 포함하세요
                    - 모든 측정값은 센티미터(cm) 단위입니다
                    
                    다음 JSON 형식으로 응답해주세요:
                    {
                        "sizes": [
                            {
                                "size": "실제사이즈",
                                "measurements": {
                                    "총장": "실제측정값",
                                    "허리단면": "실제측정값",
                                    "엉덩이단면": "실제측정값",
                                    "허벅지단면": "실제측정값",
                                    "밑위": "실제측정값",
                                    "밑단단면": "실제측정값"
                                }
                            }
                        ]
                    }"""
                },
                {
                    "role": "user",
                    "content": f"이 URL에서 실제 상품의 사이즈표 정보를 추출해주세요: {url}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        sizes_data = {
            '사이즈': [],
            '총장 (cm)': [],
            '허리단면 (cm)': [],
            '엉덩이단면 (cm)': [],
            '허벅지단면 (cm)': [],
            '밑위 (cm)': [],
            '밑단단면 (cm)': []
        }
        
        for size_info in result['sizes']:
            sizes_data['사이즈'].append(size_info['size'])
            sizes_data['총장 (cm)'].append(size_info['measurements'].get('총장', '-'))
            sizes_data['허리단면 (cm)'].append(size_info['measurements'].get('허리단면', '-'))
            sizes_data['엉덩이단면 (cm)'].append(size_info['measurements'].get('엉덩이단면', '-'))
            sizes_data['허벅지단면 (cm)'].append(size_info['measurements'].get('허벅지단면', '-'))
            sizes_data['밑위 (cm)'].append(size_info['measurements'].get('밑위', '-'))
            sizes_data['밑단단면 (cm)'].append(size_info['measurements'].get('밑단단면', '-'))
        
        return sizes_data