html_parts.append("""
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8" />
<title>Flashcards Druckvorlage</title>
<style>
  @page {
    size: A7 landscape;
    margin: 5mm;
  }
  body {
    font-family: Arial, sans-serif;
    font-size: 9pt;
    margin: 0;
    padding: 0;
  }
  .flashcard {
    width: 105mm;
    height: 74mm;
    box-sizing: border-box;
    border: 1px solid #333;
    padding: 5mm;
    overflow: hidden;
    page-break-after: always;

    display: flex;
    flex-direction: column;
    justify-content: center;  /* center vertically */
    align-items: center;      /* center horizontally */
  }
  h3 {
    margin: 0 0 5px 0;
    font-size: 11pt;
    color: #111;
    text-align: center;
  }
  .flashcard-content {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    overflow-y: auto;
  }
  .flashcard-image {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    object-fit: contain;
  }
  ul {
    padding-left: 12px;
    margin: 0 0 5px 0;
  }
  li {
    margin-bottom: 2px;
  }
</style>
</head>
<body>
""")