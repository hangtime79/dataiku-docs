// Made with Typst
// Online (consistent fonts) https://typst.app/project/puGu5S_2G4Yz23JO6_wRWQ
// Offline https://github.com/typst/typst

#let project(title: "", abstract: [], authors: (), num: "1", body) = {
  // Set the document's basic properties.
  set document(author: authors.map(a => a.name), title: title)
  set page(numbering: num, number-align: center)
  set text(font: "New Computer Modern", lang: "en")
  show math.equation: set text(weight: 400)

  // Title row.
  align(center)[
    #block(text(weight: 700, 1.75em, title))
  ]

  // Author information.
  pad(
    top: 0.5em,
    bottom: 0.5em,
    x: 2em,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter: 1em,
      ..authors.map(author => align(center)[
        *#author.name* \
        #author.affiliation
      ]),
    ),
  )

  // Main body.
  set par(justify: true)
  //show: columns.with(2, gutter: 1.3em)

  heading(outlined: false, numbering: none, text(0.85em, smallcaps[Abstract]))
  abstract

  body

  let dy = if num == none { 0em } else { -2em }
  place(bottom + center, dy: dy, [#image("full-logo-dark-blue.svg", height: 3em)])
}