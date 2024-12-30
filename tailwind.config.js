/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}", "!./node_modules"],
  theme: {
    container: {
      center: true,
      padding: "2rem",
    },
    extend: {
      colors: {
        "primary": "#005c90",
        "link-primary": "#005c90",
        "link-primary-hover": "#00446a",
        "link-hover": "#ea580c",
        "link-dark": "#aadeff",
        //"link-primary-hover": "#f1610d",
        "primary-dark": "#00446a",
        "primary-darker": "#001e2f",
      },
    },
  },
  plugins: [],
}

