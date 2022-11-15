/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gso-blue': '#5B9BD5',
        'backdrop': 'rgba(0,0,0,0.3)'
      }
    },
    fontFamily: {
      'sans': ['Calibri', 'Helvetica', 'Candara', 'sans-serif']
    }
  },
  plugins: [],
}
