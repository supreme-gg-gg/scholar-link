/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
    fontFamily: {
      Fustat: ['Fustat', 'sans-serif'],
    },
  },
  plugins: [require("daisyui")],
}
