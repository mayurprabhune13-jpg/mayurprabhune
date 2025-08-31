<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link crossorigin="" href="https://fonts.gstatic.com/" rel="preconnect"/>
<link as="style" href="https://fonts.googleapis.com/css2?display=swap&amp;family=Inter%3Awght%40400%3B500%3B700%3B900&amp;family=Noto+Sans%3Awght%40400%3B500%3B700%3B900" onload="this.rel='stylesheet'" rel="stylesheet"/>
<title>Stitch Design</title>
<link href="data:image/x-icon;base64," rel="icon" type="image/x-icon"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<style type="text/tailwindcss">
      :root {
        --primary-color: #1466b8;
        --cyan-accent: #00bcd4;
        --fuchsia-accent: #f0f;
      }
      .blog-post-card {
        @apply transform transition-transform duration-300 hover:scale-105;
      }
      .hamburger-icon span {
        @apply block h-0.5 w-6 bg-white transition-all duration-300;
      }
      .hamburger-icon.open span:nth-child(1) {
        @apply transform rotate-45 translate-y-1.5;
      }
      .hamburger-icon.open span:nth-child(2) {
        @apply opacity-0;
      }
      .hamburger-icon.open span:nth-child(3) {
        @apply transform -rotate-45 -translate-y-1.5;
      }
    </style>
</head>
<body class="bg-[#111418] font-sans">
<div class="relative flex size-full min-h-screen flex-col bg-[#111418] dark group/design-root overflow-x-hidden" style='font-family: Inter, "Noto Sans", sans-serif;'>
<div class="layout-container flex h-full grow flex-col">
<header class="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#293038] px-4 sm:px-6 lg:px-10 py-4">
<div class="flex items-center gap-4 text-white">
<svg class="h-8 w-8 text-[var(--cyan-accent)]" fill="currentColor" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
<path d="M42.1739 20.1739L27.8261 5.82609C29.1366 7.13663 28.3989 10.1876 26.2002 13.7654C24.8538 15.9564 22.9595 18.3449 20.6522 20.6522C18.3449 22.9595 15.9564 24.8538 13.7654 26.2002C10.1876 28.3989 7.13663 29.1366 5.82609 27.8261L20.1739 42.1739C21.4845 43.4845 24.5355 42.7467 28.1133 40.548C30.3042 39.2016 32.6927 37.3073 35 35C37.3073 32.6927 39.2016 30.3042 40.548 28.1133C42.7467 24.5355 43.4845 21.4845 42.1739 20.1739Z"></path>
</svg>
<h1 class="text-white text-xl font-bold tracking-tight">Mayur Prabhune</h1>
</div>
<nav class="hidden lg:flex items-center gap-6" id="desktop-nav">
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-sm font-medium transition-colors" href="#">Home</a>
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-sm font-medium transition-colors" href="#">About</a>
<a class="text-[var(--fuchsia-accent)] text-sm font-semibold leading-normal" href="#">Blog</a>
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-sm font-medium transition-colors" href="#">Services</a>
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-sm font-medium transition-colors" href="#">Contact</a>
<button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-md h-10 px-5 bg-[var(--cyan-accent)] text-black text-sm font-bold leading-normal tracking-[0.015em] hover:bg-cyan-500 transition-colors">
<span class="truncate">Book a Call</span>
</button>
</nav>
<div class="lg:hidden">
<button class="hamburger-icon z-50 p-2" id="hamburger-button">
<span class="space-y-1.5"></span>
<span class="space-y-1.5"></span>
<span class="space-y-1.5"></span>
</button>
</div>
</header>
<div class="hidden lg:hidden absolute top-0 left-0 w-full h-screen bg-[#111418] z-40 flex flex-col items-center justify-center gap-8" id="mobile-menu">
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-2xl font-medium transition-colors" href="#">Home</a>
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-2xl font-medium transition-colors" href="#">About</a>
<a class="text-[var(--fuchsia-accent)] text-2xl font-semibold leading-normal" href="#">Blog</a>
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-2xl font-medium transition-colors" href="#">Services</a>
<a class="text-gray-300 hover:text-[var(--fuchsia-accent)] text-2xl font-medium transition-colors" href="#">Contact</a>
<button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-md h-12 px-8 bg-[var(--cyan-accent)] text-black text-lg font-bold leading-normal tracking-[0.015em] hover:bg-cyan-500 transition-colors mt-4">
<span class="truncate">Book a Call</span>
</button>
</div>
<main class="px-4 sm:px-6 lg:px-10 flex flex-1 justify-center py-10 lg:py-16">
<div class="layout-content-container flex flex-col max-w-7xl flex-1">
<div class="text-center mb-12">
<h2 class="text-white tracking-tight text-4xl md:text-5xl font-bold leading-tight">From the Blog</h2>
<p class="text-[#9dabb8] text-lg mt-4 max-w-2xl mx-auto">
              Dive into the world of AI with insights and updates on machine learning, data science, and ethical considerations.
            </p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
<div class="flex flex-col gap-4 bg-[#1a1f24] p-6 rounded-lg border border-[#293038] shadow-lg blog-post-card">
<img alt="Abstract image representing AI Ethics" class="w-full h-48 object-cover rounded-md mb-4" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAeDTqGHe9lynr64tcpbI9TVlIt7CeIC369kYfn91UZecEJWuIDGnYzLV1eo1LCDzrf2_Oea_80PBZ-RLp798LQLjb_uWDraQa3sIyaq-Ua1AOQgdEVRcrPaQWE4OZaedDoC3VPg3jTr4WLPVhwk1GOMvp9CoPgHB_j0nmUsSd3wBNp5lPvolrxbhuYMmh44CMPhEp3k5Nkv0gdWBtacusP5AN4G83VtnHnfD_5mfXr7-NawCOjXsfPrvIQKeWXx0MN2PVE13cB1jr-"/>
<div class="flex flex-col gap-2">
<p class="text-sm font-medium text-[var(--cyan-accent)]">AI Ethics • Jan 15, 2024</p>
<h3 class="text-white text-xl font-bold">Navigating the Ethical Landscape of AI</h3>
<p class="text-[#9dabb8] text-base leading-relaxed">
                  Explore the critical ethical considerations in AI development and deployment, ensuring fairness, transparency, and accountability.
                </p>
</div>
<a class="inline-flex items-center text-sm font-medium text-white hover:text-[var(--fuchsia-accent)] mt-auto group" href="#">
                Read More
                <svg class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
</a>
</div>
<div class="flex flex-col gap-4 bg-[#1a1f24] p-6 rounded-lg border border-[#293038] shadow-lg blog-post-card">
<img alt="Abstract image representing Machine Learning" class="w-full h-48 object-cover rounded-md mb-4" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCykcmX4dLOkylA5qK78q7IWNRs2W3rVDfF3RF_pFMWx6NVgZsKCBMtQxyAVpgUbrwf6-5eLkYiUa3GsZhRUNsi4u0tKyItBltIXg6BfzmKb0R4yiFlYKKDdIKEj4XaXd7hLoRNqOBLe4iwomq580sdnw4jVxS0OZgj8tjDd-uyrWLqmtSeCqSkWpSrl48kq8jm-U_cdzB3dACFfrmywNQD-EGWvd0V1BxwwaPfqBIAkJ-kkRZKOn4EZiXEAGq7E-aN-PQRYukrRHR9"/>
<div class="flex flex-col gap-2">
<p class="text-sm font-medium text-[var(--cyan-accent)]">Machine Learning • Dec 28, 2023</p>
<h3 class="text-white text-xl font-bold">Demystifying Machine Learning Algorithms</h3>
<p class="text-[#9dabb8] text-base leading-relaxed">
                  A comprehensive guide to understanding and implementing various machine learning algorithms, from linear regression to neural networks.
                </p>
</div>
<a class="inline-flex items-center text-sm font-medium text-white hover:text-[var(--fuchsia-accent)] mt-auto group" href="#">
                Read More
                <svg class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
</a>
</div>
<div class="flex flex-col gap-4 bg-[#1a1f24] p-6 rounded-lg border border-[#293038] shadow-lg blog-post-card">
<img alt="Abstract image representing Data Science" class="w-full h-48 object-cover rounded-md mb-4" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBh-PTriADP84fxbVF-gOtbAyHJhN04vO4bNuIvaDmofWFbV0gU_BdlyGwi08PvMOdhnpK2Ot2sya5GvAaUAVJ4JwBrw4r-OOHPSosGZLQDGixPM-JXyUM_ffgVYqM-MfxcifZ40fOJPy9bPsHI-ThRmM_BY3l8piOjaCgt7evgloqs8wJq8XWFx6sUFNIP-jiabO-HaW_0TtiQUJxCsvXusXmGOxJhL2kH64w-7jFOW_K8HPy6A0X1Ma9ZnFQ2w_SsX841hAt3Lsze"/>
<div class="flex flex-col gap-2">
<p class="text-sm font-medium text-[var(--cyan-accent)]">Data Science • Dec 05, 2023</p>
<h3 class="text-white text-xl font-bold">The Power of Data-Driven Decision Making</h3>
<p class="text-[#9dabb8] text-base leading-relaxed">
                  Learn how to leverage data science techniques to extract valuable insights, make informed decisions, and drive business growth.
                </p>
</div>
<a class="inline-flex items-center text-sm font-medium text-white hover:text-[var(--fuchsia-accent)] mt-auto group" href="#">
                Read More
                <svg class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
</a>
</div>
<div class="flex flex-col gap-4 bg-[#1a1f24] p-6 rounded-lg border border-[#293038] shadow-lg blog-post-card">
<img alt="Abstract image representing AI Applications" class="w-full h-48 object-cover rounded-md mb-4" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC6cE8F3a0qqsVjsh-RceFDyDa6HIhZaYxRAUTQTBYu8zYR6muWkU04ePJw1KfCmBMgYrkacpTM8TDT7x4dfRSnp4zlUw3cGyUuZZ84a6PsVGqNKWA3KDXJBu6C5NJo1cQLftnIExNdxQY3fMp5_FoGA1CzbptFAij0smQetqVM2gKsUUsJOCdsSDiC3HOljoj8XndTY4jHpAgSGJO1ph_THPZ9gYbe-4i3KgjD3MPVh5oiv6RtXkqBRFB-zwqQ3ZFKeggzRAUL_xHz"/>
<div class="flex flex-col gap-2">
<p class="text-sm font-medium text-[var(--cyan-accent)]">AI Applications • Nov 18, 2023</p>
<h3 class="text-white text-xl font-bold">Real-World Applications of AI</h3>
<p class="text-[#9dabb8] text-base leading-relaxed">
                  Discover how AI is transforming industries, from healthcare and finance to transportation and entertainment, with practical examples.
                </p>
</div>
<a class="inline-flex items-center text-sm font-medium text-white hover:text-[var(--fuchsia-accent)] mt-auto group" href="#">
                Read More
                <svg class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
</a>
</div>
<div class="flex flex-col gap-4 bg-[#1a1f24] p-6 rounded-lg border border-[#293038] shadow-lg blog-post-card">
<img alt="Abstract image representing AI Trends" class="w-full h-48 object-cover rounded-md mb-4" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAzuILTX6FcLcuaD7ns6ck6Wkv2t3ZEVrLLw3x5cHYj1WkiPGDSqhs_WWoDx101JZCM3qY90bsPthvxoFLN79ANtEpI_kB0mjrs8OjdqGAH0Tm8_a2ibcOY0uzOTWgPlOQfyMvVqCEPuUF2EtNlVOjemeq-AcZBIsfdAviFpNJBzGtr3eUAqdqAqfZyHz7HAzgL7NMa9DU9fQjm3yxWAYrHJn5iVEnEjkOxbt-Roa7TnokAvkDtZ5HZNkaBzoueOxWiszQjaK2jMqPM"/>
<div class="flex flex-col gap-2">
<p class="text-sm font-medium text-[var(--cyan-accent)]">AI Trends • Oct 30, 2023</p>
<h3 class="text-white text-xl font-bold">Emerging Trends in Artificial Intelligence</h3>
<p class="text-[#9dabb8] text-base leading-relaxed">
                  Stay ahead of the curve with the latest trends in AI, including advancements in NLP, computer vision, and reinforcement learning.
                </p>
</div>
<a class="inline-flex items-center text-sm font-medium text-white hover:text-[var(--fuchsia-accent)] mt-auto group" href="#">
                Read More
                <svg class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
</a>
</div>
<div class="flex flex-col gap-4 bg-[#1a1f24] p-6 rounded-lg border border-[#293038] shadow-lg blog-post-card">
<img alt="Abstract futuristic image" class="w-full h-48 object-cover rounded-md mb-4" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB2n7e8-o8x_gK38y-QxJ9T0xW3Q1C3F7b9R2n6P0Z3N7v8C6L8R7F6H5T4O1M9K_a2Z3P9N1T5R8V0s7T4w6b6d5g4a3e2c1b0"/>
<div class="flex flex-col gap-2">
<p class="text-sm font-medium text-[var(--cyan-accent)]">Future of AI • Sep 12, 2023</p>
<h3 class="text-white text-xl font-bold">AI's Impact on the Future of Work</h3>
<p class="text-[#9dabb8] text-base leading-relaxed">
                  An analysis of how artificial intelligence is reshaping industries and what it means for the future workforce and job markets.
                </p>
</div>
<a class="inline-flex items-center text-sm font-medium text-white hover:text-[var(--fuchsia-accent)] mt-auto group" href="#">
                Read More
                <svg class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
</svg>
</a>
</div>
</div>
</div>
</main>
</div>
</div>
<script>
    const hamburgerButton = document.getElementById('hamburger-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const body = document.body;
    hamburgerButton.addEventListener('click', () => {
      hamburgerButton.classList.toggle('open');
      mobileMenu.classList.toggle('hidden');
      body.classList.toggle('overflow-hidden');
    });
  </script>

</body></html>