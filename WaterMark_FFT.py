import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import filedialog

# Tkinter 초기화
root = tk.Tk()
root.withdraw()  # Tkinter 창 숨기기

# 파일 선택 대화 상자를 열어 이미지 파일 선택
image_path = filedialog.askopenfilename(
    title="첫 번째 이미지 선택", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")]
)
image_path_2 = filedialog.askopenfilename(
    title="워터마크 이미지 선택", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")]
)


# 첫 번째 이미지 열기 및 그레이스케일로 변환
image = Image.open(image_path).convert("L")  # 흑백(그레이스케일) 변환
image_array = np.array(image)

# 두 번째 이미지 열기 및 그레이스케일로 변환
watermark_image = Image.open(image_path_2).convert("L")
watermark_array = np.array(watermark_image)

# 이미지 푸리에 변환
f_transform = np.fft.fft2(image_array)
f_shift_view = np.fft.fftshift(f_transform)  # 중심을 이동하여 저주파가 중앙에 오도록 함
magnitude_spectrum_view = 20 * np.log(
    np.abs(f_shift_view)
)  # 스펙트럼의 크기를 로그 스케일로 변환

f_shift = np.fft.fftshift(f_transform)  # 중심을 이동하여 저주파가 중앙에 오도록 함
magnitude_spectrum = np.abs(f_shift)
phase_spectrum = np.angle(f_shift)  # 위상 정보 추출


# 두 번째 이미지 푸리에 변환
f_transform_2 = np.fft.fft2(watermark_array)
f_shift_2_view = np.fft.fftshift(f_transform_2)
magnitude_spectrum_2_view = 20 * np.log(np.abs(f_shift_2_view))

f_shift_2 = np.fft.fftshift(f_transform_2)
magnitude_spectrum_2 = np.abs(f_shift_2)
phase_spectrum_2 = np.angle(f_shift_2)  # 워터마크 이미지의 위상 정보 추출

# 크기 스펙트럼 합성 (두 이미지의 크기 스펙트럼을 합침)
combined_magnitude_spectrum_view = np.sqrt(
    magnitude_spectrum_view**2 + magnitude_spectrum_2_view**2
)

# 워터마크 크기 스펙트럼의 강도를 줄여서 합성
alpha = 0.1  # 워터마크의 강도를 조절하는 파라미터
combined_magnitude_spectrum = magnitude_spectrum + alpha * magnitude_spectrum_2

# 새로운 주파수 영역 생성 (크기 스펙트럼 합성 + 기존 위상 정보 유지)
combined_f_shift = combined_magnitude_spectrum * np.exp(1j * phase_spectrum)

# 역푸리에 변환하여 이미지 복원
combined_f = np.fft.ifftshift(combined_f_shift)  # 역푸리에 변환 전, shift 복원
combined_image_array = np.fft.ifft2(combined_f)  # 역푸리에 변환
combined_image_array = np.abs(
    combined_image_array
)  # 복소수 부분을 제거하고 절댓값 사용


# 주파수 영역으로 변환된 이미지 확인
f_transform_combined = np.fft.fft2(combined_image_array)
f_shift_combined = np.fft.fftshift(
    f_transform_combined
)  # 중심을 이동하여 저주파가 중앙에 오도록 함
magnitude_spectrum_combined = np.abs(f_shift_combined)
magnitude_spectrum_combined_log = 20 * np.log(
    magnitude_spectrum_combined
)  # 로그 스케일로 변환

# magnitude_spectrum_2 복원 (combined에서 magnitude_spectrum을 빼고 alpha로 나눔)
magnitude_spectrum_2_reconstructed = (
    magnitude_spectrum_combined - magnitude_spectrum
) / alpha

magnitude_spectrum_2_reconstructed_log = 20 * np.log(
    magnitude_spectrum_2_reconstructed
)  # 로그 스케일로 변환

# reconstructed magnitude_spectrum_2를 주파수 영역에서 합성
combined_f_shift_reconstructed = (
    alpha * magnitude_spectrum_2_reconstructed * np.exp(1j * phase_spectrum_2)
)

# 역푸리에 변환하여 복원된 이미지 생성
combined_f_reconstructed = np.fft.ifftshift(
    combined_f_shift_reconstructed
)  # 역푸리에 변환 전, shift 복원
combined_image_array_reconstructed = np.fft.ifft2(
    combined_f_reconstructed
)  # 역푸리에 변환
combined_image_array_reconstructed = np.abs(
    combined_image_array_reconstructed
)  # 복소수 부분 제거하고 절댓값 사용


# 각 플롯을 준비합니다. (여기서는 간단히 빈 플롯으로 예시를 듭니다.)
def plot_figure(figure_number):
    # 현재 figure를 지우지 않고 플롯만 갱신합니다.
    plt.cla()  # 현재 Axes를 지웁니다.
    plt.clf()  # figure 자체를 지우지 않습니다.

    if figure_number == 1:
        # 첫 번째 플롯
        # 버튼 생성 (단, 여기서 한 번만 생성하고 그 이후로는 재사용)
        ax_prev = plt.axes([0.7, 0.01, 0.1, 0.075])  # 'Previous' 버튼 위치 및 크기 설정
        btn_prev = Button(ax_prev, "Previous")  # 'Previous' 버튼 생성
        btn_prev.on_clicked(previous_plot)  # 'Previous' 버튼 클릭 시 previous_plot 호출

        ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])  # 'Next' 버튼 위치 및 크기 설정
        btn_next = Button(ax_next, "Next")  # 'Next' 버튼 생성
        btn_next.on_clicked(next_plot)  # 'Next' 버튼 클릭 시 next_plot 호출
        plt.subplot(1, 2, 1)
        plt.imshow(image_array, cmap="gray")
        plt.title("Original Image (Lena)")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(magnitude_spectrum_view, cmap="gray")
        plt.title("Fft Spectrum\n (Frequency Domain - Lena)")
        plt.axis("off")

    elif figure_number == 2:
        # 두 번째 플롯
        # 버튼 생성 (단, 여기서 한 번만 생성하고 그 이후로는 재사용)
        ax_prev = plt.axes([0.7, 0.01, 0.1, 0.075])  # 'Previous' 버튼 위치 및 크기 설정
        btn_prev = Button(ax_prev, "Previous")  # 'Previous' 버튼 생성
        btn_prev.on_clicked(previous_plot)  # 'Previous' 버튼 클릭 시 previous_plot 호출

        ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])  # 'Next' 버튼 위치 및 크기 설정
        btn_next = Button(ax_next, "Next")  # 'Next' 버튼 생성
        btn_next.on_clicked(next_plot)  # 'Next' 버튼 클릭 시 next_plot 호출
        plt.subplot(1, 2, 1)
        plt.imshow(watermark_array, cmap="gray")
        plt.title("Watermark Image")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(magnitude_spectrum_2_view, cmap="gray")
        plt.title("Fft Spectrum\n (Frequency Domain - Watermark)")
        plt.axis("off")

    elif figure_number == 3:
        # 세 번째 플롯
        # 버튼 생성 (단, 여기서 한 번만 생성하고 그 이후로는 재사용)
        ax_prev = plt.axes([0.7, 0.01, 0.1, 0.075])  # 'Previous' 버튼 위치 및 크기 설정
        btn_prev = Button(ax_prev, "Previous")  # 'Previous' 버튼 생성
        btn_prev.on_clicked(previous_plot)  # 'Previous' 버튼 클릭 시 previous_plot 호출

        ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])  # 'Next' 버튼 위치 및 크기 설정
        btn_next = Button(ax_next, "Next")  # 'Next' 버튼 생성
        btn_next.on_clicked(next_plot)  # 'Next' 버튼 클릭 시 next_plot 호출
        plt.subplot(1, 3, 1)
        plt.imshow(magnitude_spectrum_view, cmap="gray")
        plt.title("Fft Spectrum\n (Frequency Domain - Lena)")
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.imshow(magnitude_spectrum_2_view, cmap="gray")
        plt.title("Fft Spectrum\n (Frequency Domain - Watermark)")
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.imshow(combined_magnitude_spectrum_view, cmap="gray")
        plt.title("Combined Fft Spectrum\n (Lena + Watermark)")
        plt.axis("off")

    elif figure_number == 4:
        # 네 번째 플롯
        # 버튼 생성 (단, 여기서 한 번만 생성하고 그 이후로는 재사용)
        ax_prev = plt.axes([0.7, 0.01, 0.1, 0.075])  # 'Previous' 버튼 위치 및 크기 설정
        btn_prev = Button(ax_prev, "Previous")  # 'Previous' 버튼 생성
        btn_prev.on_clicked(previous_plot)  # 'Previous' 버튼 클릭 시 previous_plot 호출

        ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])  # 'Next' 버튼 위치 및 크기 설정
        btn_next = Button(ax_next, "Next")  # 'Next' 버튼 생성
        btn_next.on_clicked(next_plot)  # 'Next' 버튼 클릭 시 next_plot 호출
        plt.subplot(1, 3, 1)
        plt.imshow(image_array, cmap="gray")
        plt.title("Original Image (Lena)")
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.imshow(watermark_array, cmap="gray")
        plt.title("Watermark Image")
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.imshow(combined_image_array, cmap="gray")
        plt.title("Watermarked Image (Combined)")
        plt.axis("off")

    elif figure_number == 5:
        # 다섯 번째 플롯
        # 버튼 생성 (단, 여기서 한 번만 생성하고 그 이후로는 재사용)
        ax_prev = plt.axes([0.7, 0.01, 0.1, 0.075])  # 'Previous' 버튼 위치 및 크기 설정
        btn_prev = Button(ax_prev, "Previous")  # 'Previous' 버튼 생성
        btn_prev.on_clicked(previous_plot)  # 'Previous' 버튼 클릭 시 previous_plot 호출

        ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])  # 'Next' 버튼 위치 및 크기 설정
        btn_next = Button(ax_next, "Next")  # 'Next' 버튼 생성
        btn_next.on_clicked(next_plot)  # 'Next' 버튼 클릭 시 next_plot 호출
        plt.subplot(1, 4, 1)
        plt.imshow(magnitude_spectrum_combined_log, cmap="gray")
        plt.title("Watermarked Image\n fft_New (Combined)")
        plt.axis("off")

        plt.subplot(1, 4, 2)
        plt.imshow(magnitude_spectrum_2_reconstructed_log, cmap="gray")
        plt.title("Extracted watermarks fft")
        plt.axis("off")

        plt.subplot(1, 4, 3)
        plt.imshow(watermark_array, cmap="gray")
        plt.title("Watermark Image (org)")
        plt.axis("off")

        plt.subplot(1, 4, 4)
        plt.imshow(combined_image_array_reconstructed, cmap="gray")
        plt.title("Watermarked Image (Extracted)")
        plt.axis("off")

    plt.draw()  # 그린 후 figure 갱신


# 버튼 클릭 시 해당 플롯을 표시하는 함수
def next_plot(event):
    global plot_index
    plot_index += 1
    if plot_index > 5:
        plot_index = 1
    plot_figure(plot_index)


# 버튼 클릭 시 해당 플롯을 표시하는 함수
def previous_plot(event):
    global plot_index
    plot_index -= 1
    if plot_index < 1:
        plot_index = 5
    plot_figure(plot_index)


# 초기 plot index 설정
plot_index = 1

# 창 크기 설정
plt.figure(figsize=(12, 6))  # 창 크기를 원하는 크기로 설정 (예: 16x8)

# 초기 plot 그리기
plot_figure(plot_index)

# 버튼 생성 (단, 여기서 한 번만 생성하고 그 이후로는 재사용)
ax_prev = plt.axes([0.7, 0.01, 0.1, 0.075])  # 'Previous' 버튼 위치 및 크기 설정
btn_prev = Button(ax_prev, "Previous")  # 'Previous' 버튼 생성
btn_prev.on_clicked(previous_plot)  # 'Previous' 버튼 클릭 시 previous_plot 호출

ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])  # 'Next' 버튼 위치 및 크기 설정
btn_next = Button(ax_next, "Next")  # 'Next' 버튼 생성
btn_next.on_clicked(next_plot)  # 'Next' 버튼 클릭 시 next_plot 호출

# 버튼은 이미 생성된 상태에서 이후 플롯만 그리기
plt.show()
