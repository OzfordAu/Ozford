/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}", "!./node_modules"],
  theme: {
    container: {
      center: true,
      padding: "1rem",
    },
    extend: {
      colors: {
        "primary": "#1a305b",
        "link-primary": "#1a305b",
        "link-primary-hover": "#294886",
        "link-hover": "#ea580c",
        "link-dark": "#aadeff",
        //"link-primary-hover": "#f1610d",
        "primary-dark": "#1a305b",
        "primary-darker": "#1a305b",
        "secondary": "#E8C52A",
        "secondary-dark": "#bb9f22",
      },
      fontFamily: {
        primary: ['Nohemi', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

