// Game content: places on the map, police units, and the calls.
// Adding a scene = one video in src/assets/video, a few audio lines in
// tools/make_audio.py and one entry in SCENES.

export const PLACES = {
  neighborhood: { id: "neighborhood", name: "שכונת הגפן",     sub: "רחוב הגפן 12",     icon: "🏘️", x: 160, y: 130 },
  mall:         { id: "mall",         name: "קניון השוק",     sub: "מרכז מסחרי",       icon: "🏬", x: 470, y: 110 },
  parking:      { id: "parking",      name: "החניון המרכזי",  sub: "חניון ציבורי",     icon: "🅿️", x: 780, y: 130 },
  downtown:     { id: "downtown",     name: "רחוב הרצל",      sub: "מרכז העיר",        icon: "🏙️", x: 160, y: 330 },
  junction:     { id: "junction",     name: "צומת העצמאות",   sub: "צומת מרומזר",      icon: "🚦", x: 470, y: 320 },
  park:         { id: "park",         name: "פארק העיר",      sub: "שער ראשי",         icon: "🌳", x: 780, y: 330 },
  garden:       { id: "garden",       name: "גינת הפרחים",    sub: "גינה ציבורית",     icon: "🌷", x: 300, y: 450 },
};

export const STATION = { x: 640, y: 480, name: "תחנת משטרה", icon: "🏢" };

export const UNITS = {
  patrol:    { id: "patrol",    code: "ניידת 21",   name: "ניידת סיור",   icon: "🚓", desc: "פריצות, גניבות, אירועים כלליים" },
  moto:      { id: "moto",      code: "אופנוע 7",   name: "אופנוע משטרה", icon: "🏍️", desc: "מרדף מהיר, חשוד שברח" },
  traffic:   { id: "traffic",   code: "תנועה 4",    name: "ניידת תנועה",  icon: "🚔", desc: "עבירות תנועה, כבישים וצמתים" },
  community: { id: "community", code: "קהילתי 12",  name: "שוטר קהילתי",  icon: "👮", desc: "עזרה לאזרחים, ילדים ובעלי חיים" },
};

export const RANKS = [
  { min: 0,    name: "שוטר",   short: "שוטר" },
  { min: 300,  name: "סמל",    short: "סמל" },
  { min: 700,  name: "רס\"ר",  short: "רס\"ר" },
  { min: 1200, name: "קצין",   short: "קצין" },
  { min: 2000, name: "מפקד",   short: "מפקד" },
];

export const AVATARS = [
  { id: "a1", icon: "👮‍♂️", name: "שוטר" },
  { id: "a2", icon: "👮‍♀️", name: "שוטרת" },
  { id: "a3", icon: "🕵️", name: "בלש" },
  { id: "a4", icon: "🐕‍🦺", name: "יחידת כלבנים" },
];

// priority: 1 = urgent (red), 2 = high (orange), 3 = routine (blue)
export const SCENES = [
  {
    id: "home_burglary", code: "פריצה לדירה", priority: 1,
    title: "פריצה לדירה ברחוב הגפן",
    callerIcon: "🧑", callerName: "שכן, רחוב הגפן",
    place: "neighborhood", unit: "patrol", okUnits: ["moto"],
    what:   { icon: "🥷", text: "פורץ נכנס לדירה" },
    who:    { icon: "🏠", text: "בעלי הדירה" },
    action: { icon: "🚓", text: "לתפוס את הפורץ ולאבטח את הדירה" },
  },
  {
    id: "shop_breakin", code: "פריצה לעסק", priority: 1,
    title: "פריצה לחנות בקניון השוק",
    callerIcon: "💂", callerName: "שומר לילה, קניון השוק",
    place: "mall", unit: "patrol", okUnits: ["moto"],
    what:   { icon: "🔓", text: "פורץ פותח מנעול של חנות בלילה" },
    who:    { icon: "🏪", text: "בעל החנות" },
    action: { icon: "🛑", text: "לתפוס את הפורץ לפני שייכנס" },
  },
  {
    id: "car_breakin", code: "פריצה לרכב", priority: 2,
    title: "פריצה לרכב בחניון המרכזי",
    callerIcon: "👴", callerName: "שומר החניון",
    place: "parking", unit: "patrol", okUnits: ["moto"],
    what:   { icon: "🚗", text: "מישהו פורץ למכונית" },
    who:    { icon: "🔑", text: "בעל הרכב" },
    action: { icon: "🚓", text: "לתפוס את הפורץ בחניון" },
  },
  {
    id: "bag_snatch", code: "חטיפת תיק", priority: 1,
    title: "חטיפת תיק ברחוב הרצל",
    callerIcon: "👩", callerName: "עוברת אורח, רחוב הרצל",
    place: "downtown", unit: "moto", okUnits: ["patrol"],
    what:   { icon: "👜", text: "מישהו חטף תיק מאישה וברח" },
    who:    { icon: "🙍‍♀️", text: "האישה שהתיק שלה נחטף" },
    action: { icon: "🏍️", text: "לרדוף אחרי החוטף ולהחזיר את התיק" },
  },
  {
    id: "lost_child", code: "ילד לבד", priority: 2,
    title: "ילד לבד בפארק העיר",
    callerIcon: "👩‍🦱", callerName: "מטיילת בפארק",
    place: "park", unit: "community", okUnits: ["patrol"],
    what:   { icon: "🧒", text: "ילד קטן נמצא לבד בלי הורים" },
    who:    { icon: "👶", text: "הילד" },
    action: { icon: "👨‍👩‍👦", text: "להישאר עם הילד ולמצוא את ההורים" },
  },
  {
    id: "cat_tree", code: "חילוץ בעל חיים", priority: 3,
    title: "חתול תקוע על עץ בגינת הפרחים",
    callerIcon: "👧", callerName: "ילדה מהגינה",
    place: "garden", unit: "community", okUnits: ["patrol"],
    what:   { icon: "🐱", text: "חתול תקוע על עץ וכלב מתחתיו" },
    who:    { icon: "🐈", text: "החתול" },
    action: { icon: "🪜", text: "להרחיק את הכלב ולהוריד את החתול" },
  },
  {
    id: "red_light", code: "עבירת תנועה", priority: 2,
    title: "נהג עבר באור אדום בצומת העצמאות",
    callerIcon: "🚶", callerName: "הולך רגל, צומת העצמאות",
    place: "junction", unit: "traffic", okUnits: ["patrol", "moto"],
    what:   { icon: "🚕", text: "מונית עברה באור אדום" },
    who:    { icon: "🚸", text: "הולכי הרגל במעבר החצייה" },
    action: { icon: "📋", text: "לעצור את הנהג ולתת לו דוח" },
  },
];

export const QUESTIONS = [
  { key: "what",   line: "report_q1", label: "מה קרה?" },
  { key: "who",    line: "report_q2", label: "מי צריך עזרה?" },
  { key: "action", line: "report_q3", label: "מה השוטרים צריכים לעשות?" },
];
