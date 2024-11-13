from PIL import Image, ImageDraw, ImageFont

# 이미지 크기 및 배경 색상 설정
width, height = 512, 512
background_color = (255, 255, 255)  # 흰색

# 흰 배경 이미지 생성
image = Image.new("RGB", (width, height), background_color)

# ImageDraw 객체 생성
draw = ImageDraw.Draw(image)

# 텍스트 및 폰트 설정
text = "202012471\n정지우"
font_size = 40  # 폰트 크기 조정

# 한글을 지원하는 폰트 설정 (Windows에서 '맑은 고딕' 사용)
try:
    font = ImageFont.truetype(
        "C:\\Windows\\Fonts\\malgun.ttf", font_size
    )  # 맑은 고딕 폰트 사용
except IOError:
    font = ImageFont.load_default()  # 기본 폰트 사용 (한글이 지원되지 않음)

# 텍스트 크기 구하기 (textbbox 사용)
bbox = draw.textbbox((0, 0), text, font=font)
text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

# 텍스트 위치 설정 (이미지 중앙에 오도록)
text_x = (width - text_width) // 2
text_y = (height - text_height) // 2

# 텍스트 추가
text_color = (0, 0, 0)  # 검은색
draw.text((text_x, text_y), text, fill=text_color, font=font)

# 이미지 보기
image.show()

# 이미지 저장 (특정 경로 지정)
image.save("C:\\Users\\PC\\Desktop\\워터마크\\watermark.png")
