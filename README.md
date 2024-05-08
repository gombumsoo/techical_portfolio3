# techical_portfolio3

## 기술 평가 항목
4. 데이터 수집 기술과 수집한 데이터 집합의 유용성 및 공개 여부
---
## 레포지토리 소개
- 본 레포지토리는 자동차 파손 이미지가 각 종류별로 레이블링된 데이터셋을 제공하고 있습니다.  
- `chrome_crawling.py` 코드를 사용하여 이미지를 수집했으며, 파손 상태에 따라 여러 키워드에 대해 크롤링을 진행했습니다.  
- 파손상태는 '긁힘', '깨짐', '유리 깨짐', '이격', '찌그러짐', '정상' 총 6개의 카테고리로 분류했습니다.

### 데이터셋 구성
- `damaged_car_classification_train_dataset.zip` : training dataset으로 2153장의 이미지로 구성되어 있습니다.
- `damaged_car_classification_test_dataset.zip` : test dataset으로 240장의 이미지로 구성되어 있습니다.

### 유용성 및 공개 여부
-  자동차 파손 부위의 분류 모델을 학습할 때 사용할 수 있으며, 파손부위에 대한 추가 레이블링을 할 경우 파손부위 탐지 모델의 학습에도 활용될 수 있습니다. 현재는 레포지토리에만 공개되어 있습니다.

### 예시 샘플
- 긁힘
![긁힘 (17)](https://github.com/gombumsoo/techical_portfolio3/assets/69720752/77de1dbb-1c7c-40e1-9530-8206cc697406)

- 깨짐
![깨짐 (8)](https://github.com/gombumsoo/techical_portfolio3/assets/69720752/e4860e17-b497-410d-9df0-59342db5eec8)

- 유리 깨짐
![유리깨짐 (2)](https://github.com/gombumsoo/techical_portfolio3/assets/69720752/d0e9743c-16c1-4416-9598-ee64edbf9566)

- 이격
![이격 (1)](https://github.com/gombumsoo/techical_portfolio3/assets/69720752/a7b40aad-6bda-4728-80af-2ef41d8156e6)

- 찌그러짐
![찌그러짐 (5)](https://github.com/gombumsoo/techical_portfolio3/assets/69720752/81236f9a-167a-4890-b402-f91f97f60264)

- 정상
![정상 (2)](https://github.com/gombumsoo/techical_portfolio3/assets/69720752/f7d36653-150c-4106-9062-7838786c34cd)

