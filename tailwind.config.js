/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}", "!./node_modules"],
  theme: {
    extend: {
      colors: {
        "primary": "#005c90",
        "link-primary": "#005c90",
        "link-primary-hover": "#00446a",
        //"link-primary-hover": "#f1610d",
        "primary-dark": "#00446a",
        "primary-darker": "#00324e",
      },
    },
  },
  plugins: [],
}

