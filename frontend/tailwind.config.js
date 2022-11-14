/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    colors: {
      'blue': '#5B9BD5',
    },
    fontFamily: {
      'sans': ['Calibri', 'Helvetica', 'Candara', 'sans-serif']
    }
  },
  plugins: [],
}
