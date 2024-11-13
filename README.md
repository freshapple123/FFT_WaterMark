# FFT Watermarking in the Frequency Domain

In this project, we apply a watermark to an image in the frequency domain using Fourier Transform techniques.

## Steps

### 1. Convert the Original Image to Frequency Domain with FFT
The original image is transformed to the frequency domain using the Fast Fourier Transform (FFT). For better visualization, the logarithmic scale is applied.

![Original Image in Frequency Domain](https://github.com/user-attachments/assets/90fed654-c1f2-4946-9623-e280ceaab28e)

### 2. Convert the Watermark Image to Frequency Domain
Similarly, the watermark image is transformed to the frequency domain.

![Watermark Image in Frequency Domain](https://github.com/user-attachments/assets/9fb7729f-41b7-4192-9cd0-d7c079465fb3)

### 3. Merge the Frequency Domain Images
The original and watermark images in the frequency domain are combined. The image below shows a 1:1 ratio for visual purposes; however, this ratio needs to be adjusted to avoid excessive transformations in the embedded image.

![Merged Frequency Domain Image](https://github.com/user-attachments/assets/4d931b89-89bf-43ff-aff8-a03f99299c0b)

### 4. Apply the Watermarked Image in the Spatial Domain
The merged frequency domain image is transformed back to the spatial domain to apply the watermark visibly.

![Watermarked Image in Spatial Domain](https://github.com/user-attachments/assets/06348dcd-4043-4a72-a659-90437ffff8a7)

### 5. Extract the Watermark
The watermarked image is transformed back to the frequency domain, from which the watermark’s frequency domain information is extracted. This is then transformed back to the spatial domain for visualization.

![Extracted Watermark in Spatial Domain](https://github.com/user-attachments/assets/2a68142d-978e-446f-9bc8-ff15052519d1)

---

Through this process, the watermark can be embedded and later extracted by using transformations in the frequency domain. This method provides an effective and less intrusive approach to watermarking images.
