/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
    fontFamily: {
      generalsans: ['GeneralSans', 'sans-serif'],
    },
  },
  plugins: [require("daisyui")],
}
