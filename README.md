# מוקד 100 - משחק שוטרים לילדים

תוכנת Windows (Tauri v2) שמדמה מערכת שליטה ובקרה של מוקד משטרתי. הילד עונה לקריאות,
צופה במצלמות אבטחה, מסמן את מקום האירוע במפה, שולח כוח מתאים, ממלא דוח אירוע
ומקבל ציון ממפקד התחנה. הכל בלחיצות בלבד, עם קריינות בעברית.

## הורדה והתקנה
כל דחיפה ל-`main` בונה קובץ התקנה ב-GitHub Actions (Actions > Build Windows installer > Artifacts).
תיוג `vX.Y.Z` יוצר Release עם קובץ `Moked100_X.Y.Z_x64-setup.exe`.
ההתקנה לא דורשת הרשאות מנהל ולא דורשת התקנות מקדימות: מריצים את ה-exe ובוחרים תיקייה. אם במחשב חסר רכיב WebView2 (נדיר, קיים בכל Windows 10/11 מעודכן), המתקין מתקין אותו לבד.

## מבנה
```
src/                 הממשק (HTML/CSS/JS, בלי bundler)
  js/content.js      תוכן המשחק: מקומות, כוחות, אירועים, שאלות הדוח
  js/app.js          לוגיקת המשחק
  data/lines.json    טקסט הקריינות (נוצר אוטומטית)
  assets/video       סרטוני מצלמות אבטחה + תמונות פוסטר
  assets/audio       קריינות ואפקטים
src-tauri/           קוד Rust (שמירת התקדמות בתיקיית AppData)
tools/
  process_stock.py   הורדה ועיבוד של סרטוני סטוק לסגנון CCTV
  make_audio.py      יצירת קריינות (edge-tts) ואפקטים
  make_icon.py       אייקון האפליקציה
```

## הוספת אירוע חדש
1. הוסיפו ערך ל-`CLIPS` ב-`tools/process_stock.py` (או הניחו קובץ משלכם ב-`tools/_work/<id>.mp4`) והריצו את הסקריפט.
2. הוסיפו שורות `call_<id>`, `done_<id>` ו-`OPTIONS[<id>]` ב-`tools/make_audio.py` והריצו `python3 tools/make_audio.py tts`.
3. הוסיפו את האירוע ל-`SCENES` ב-`src/js/content.js`.

## פיתוח מקומי
```
npm install
npx tauri dev
```
לבדיקה בדפדפן בלבד: `python3 -m http.server 8765 --directory src` ולפתוח `http://localhost:8765`.

## ניקוד
מענה מהיר לשיחה (10), סימון מקום האירוע (30), בחירת הכוח (30), דוח אירוע (30).
85 ומעלה = 3 כוכבים, 60 ומעלה = 2, אחרת 1. דרגות: שוטר, סמל, רס"ר, קצין, מפקד.
