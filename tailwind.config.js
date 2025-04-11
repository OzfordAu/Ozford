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
        "primary-darker": "#0e1c36",
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

