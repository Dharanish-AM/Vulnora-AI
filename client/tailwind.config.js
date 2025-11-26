/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#6B3F69', // Deep Purple
        secondary: '#8D5F8C', // Medium Purple
        accent: '#A376A2', // Light Purple
        dark: '#2D1A2C', // Darker Deep Purple
        darker: '#1A0F19', // Deepest Purple
        card: '#FAF5F8', // Very Light Purple Tint
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
