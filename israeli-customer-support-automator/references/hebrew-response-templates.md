# Hebrew Response Templates for Customer Support

This reference contains ready-to-use Hebrew canned responses for common customer support scenarios in Israeli businesses. Templates use `{variable}` placeholders that should be replaced with actual values.

## Acknowledgment Templates

### General Acknowledgment (aishur kabala klali)

```
שלום {customer_name},

תודה שפנית אלינו. קיבלנו את פנייתך ומספר הכרטיס שלך הוא {ticket_id}.
צוות התמיכה שלנו יבדוק את הנושא ויחזור אליך בהקדם האפשרי, לכל המאוחר תוך {sla_hours} שעות עבודה.

אם יש לך מידע נוסף שיכול לעזור לנו לטפל בפנייתך, אל תהסס/י לענות להודעה זו.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### Urgent Ticket Acknowledgment (aishur pniya dchufah)

```
שלום {customer_name},

קיבלנו את פנייתך הדחופה (כרטיס {ticket_id}).
הנושא סומן בעדיפות גבוהה ונציג/ת בכיר/ה כבר מטפל/ת בו.
נחזור אליך תוך {sla_hours} שעה.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### After-Hours Auto-Response (tguva otomatit mechutz leshaot avoda)

```
שלום,

תודה שפנית ל-{company_name}.

שעות הפעילות שלנו הן ראשון עד חמישי, 08:30-17:30.
קיבלנו את פנייתך ונטפל בה ביום העבודה הבא.

לעניינים דחופים, ניתן להתקשר: {emergency_phone}

בברכה,
צוות {company_name}
```

### Friday/Shabbat Auto-Response

```
שלום,

תודה שפנית ל-{company_name}.

המשרדים שלנו סגורים כעת לכבוד שבת.
נחזור אליך ביום ראשון בבוקר.

שבת שלום,
צוות {company_name}
```

## Billing Templates

### Refund Processed (zikui butzah)

```
שלום {customer_name},

בהמשך לפנייתך (כרטיס {ticket_id}), שמחים לעדכן שביצענו זיכוי בסך {amount} ש"ח.

פרטי הזיכוי:
- סכום: {amount} ש"ח
- אמצעי תשלום: כרטיס אשראי המסתיים ב-{last_4_digits}
- מספר אסמכתא: {reference_id}
- זמן משוער להופעה בחשבון: 3-5 ימי עסקים

נשמח לעמוד לרשותך בכל שאלה נוספת.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### Billing Dispute Under Review (machloket chiyuv benidka)

```
שלום {customer_name},

קיבלנו את פנייתך לגבי חיוב בסך {amount} ש"ח מתאריך {charge_date} (כרטיס {ticket_id}).

אנחנו בודקים את הנושא ונחזור אליך עם תשובה מפורטת תוך {sla_hours} שעות עבודה.

בינתיים, אם יש ברשותך אסמכתאות נוספות (אישור הזמנה, חשבונית, צילום מסך מהבנק), נשמח לקבל אותן כדי לזרז את הטיפול.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### Duplicate Charge Refund (zikui chiyuv kful)

```
שלום {customer_name},

בדקנו את פנייתך (כרטיס {ticket_id}) ואכן מצאנו חיוב כפול בסך {amount} ש"ח.

אנו מתנצלים על אי הנוחות. ביצענו זיכוי מיידי:
- סכום הזיכוי: {amount} ש"ח
- אסמכתא: {reference_id}
- צפי להופעה בחשבון: 3-5 ימי עסקים

נקטנו בצעדים למניעת הישנות המקרה.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

## Returns and Cancellations Templates

### Return Instructions (hora'ot lehachzara)

```
שלום {customer_name},

בהתאם לבקשתך להחזרת המוצר (הזמנה {order_id}), להלן ההוראות:

1. ודאו שהמוצר באריזתו המקורית (ככל האפשר)
2. צרפו את החשבונית או אישור ההזמנה
3. שלחו לכתובת: {return_address}
   או הביאו לסניף הקרוב: {branch_address}
   בשעות: {branch_hours}

שימו לב:
- ההחזרה חייבת להתבצע תוך 14 ימים ממועד קבלת המוצר (בהתאם לחוק הגנת הצרכן)
- דמי ביטול: {cancellation_fee} ש"ח
- הזיכוי יבוצע תוך 14 ימים מקבלת המוצר

מספר אישור החזרה: {return_id}

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### Cancellation Confirmation (ishur bitul)

```
שלום {customer_name},

הזמנתך (מספר {order_id}) בוטלה בהצלחה.

פרטי הביטול:
- מספר הזמנה: {order_id}
- סכום ההזמנה: {order_amount} ש"ח
- דמי ביטול: {cancellation_fee} ש"ח
- סכום הזיכוי: {refund_amount} ש"ח
- צפי לזיכוי: תוך 14 ימים

אם יש לך שאלות נוספות, אנחנו כאן.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### Return Rejected (dchiyat bakashat hachzara)

```
שלום {customer_name},

בדקנו את בקשתך להחזרת המוצר (הזמנה {order_id}) ולצערנו לא ניתן לאשר את ההחזרה מהסיבה הבאה:

{rejection_reason}

בהתאם לחוק הגנת הצרכן, החריגים לזכות הביטול כוללים:
- מוצרים מתכלים
- מוצרים שיוצרו או שונו במיוחד עבור הלקוח
- מוצרי מידע שנפתחו (תוכנה, הקלטות)
- שירותים לתאריך מסוים

אם לדעתך ההחלטה אינה נכונה, באפשרותך:
1. להשיב להודעה זו עם מידע נוסף
2. לבקש העברה למנהל/ת צוות
3. לפנות לרשות להגנת הצרכן

נשמח לסייע בכל דרך אחרת שנוכל.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

## Technical Support Templates

### Issue Acknowledged (ba'aya hukra)

```
שלום {customer_name},

תודה שדיווחת על הבעיה (כרטיס {ticket_id}).

הבנו שאתה/את חווה: {issue_summary}

הצוות הטכני שלנו בודק את הנושא. בינתיים, אפשר לנסות:
{troubleshooting_steps}

נעדכן אותך ברגע שנמצא פתרון.

בברכה,
{agent_name}
צוות התמיכה הטכנית, {company_name}
```

### Issue Resolved (ba'aya nitpera)

```
שלום {customer_name},

שמחים לעדכן שהבעיה שדיווחת עליה (כרטיס {ticket_id}) טופלה בהצלחה.

מה נעשה: {resolution_details}

אם הבעיה חוזרת או שיש לך שאלות נוספות, אל תהסס/י לפנות אלינו.

נשמח אם תוכל/י להקדיש רגע לדירוג חוויית השירות:
{satisfaction_survey_link}

בברכה,
{agent_name}
צוות התמיכה הטכנית, {company_name}
```

### Known Issue Notification (hodaa al ba'aya yedua)

```
שלום {customer_name},

תודה שפנית אלינו (כרטיס {ticket_id}).

הנושא שדיווחת עליו הוא בעיה מוכרת שאנחנו כבר מטפלים בה.
צפי לתיקון: {estimated_fix_date}

נעדכן אותך ברגע שהתיקון ייושם. אין צורך לפתוח כרטיס נוסף.

מתנצלים על אי הנוחות.

בברכה,
{agent_name}
צוות התמיכה הטכנית, {company_name}
```

## Escalation Templates

### Escalation Notice to Customer (hodaat haslama lalakoch)

```
שלום {customer_name},

פנייתך (כרטיס {ticket_id}) הועברה לטיפול {escalation_role} שלנו.
{escalated_to_name} ייצור/תיצור איתך קשר בהקדם, לכל המאוחר תוך {sla_hours} שעות.

אנו מתייחסים לפנייתך ברצינות רבה ונעשה כל שביכולתנו לפתור את העניין לשביעות רצונך.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### Supervisor Follow-Up (ma'akav menahel)

```
שלום {customer_name},

שמי {supervisor_name} ואני {supervisor_title} בצוות שירות הלקוחות של {company_name}.

קראתי את ההתכתבות שלך (כרטיס {ticket_id}) ואני רוצה לוודא שהנושא מטופל כראוי.

{personalized_response}

אני זמין/ה באופן אישי בטלפון {supervisor_phone} או במייל {supervisor_email} אם תרצה/י לדבר ישירות.

בברכה,
{supervisor_name}
{supervisor_title}, {company_name}
```

## Shipping Templates

### Tracking Information (meidat ma'akav)

```
שלום {customer_name},

ההזמנה שלך ({order_id}) נשלחה!

פרטי המשלוח:
- חברת שילוח: {shipping_company}
- מספר מעקב: {tracking_number}
- צפי הגעה: {estimated_delivery}
- קישור למעקב: {tracking_link}

אם החבילה לא תגיע עד {latest_delivery_date}, אנא פנו אלינו.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

### Delivery Delay Apology (hitnatzlut al ikuv)

```
שלום {customer_name},

אנו מצטערים לעדכן שחלה עיכוב במשלוח ההזמנה שלך ({order_id}).

סיבת העיכוב: {delay_reason}
מועד הגעה מעודכן: {new_estimated_delivery}

אנו מתנצלים על אי הנוחות. {compensation_if_applicable}

אם אינך מעוניין/ת להמתין, נשמח לבצע זיכוי מלא.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```

## Satisfaction Survey Templates

### Post-Resolution CSAT Survey

```
שלום {customer_name},

נשמח לשמוע על חוויית השירות שלך (כרטיס {ticket_id}).

מה מידת שביעות הרצון שלך מהטיפול בפנייה?

1 - לא מרוצה כלל
2 - לא מרוצה
3 - ניטרלי
4 - מרוצה
5 - מרוצה מאוד

תגובתך עוזרת לנו להשתפר.

תודה,
צוות {company_name}
```

### NPS Survey

```
שלום {customer_name},

נשמח לשמוע את דעתך על {company_name}.

בסולם של 0 עד 10, עד כמה סביר שתמליץ/י עלינו לחבר/ה או עמית/ה?

0 (לא סביר כלל) ... 5 (ניטרלי) ... 10 (סביר מאוד)

מה הסיבה העיקרית לציון שנתת? (אופציונלי)
__________________

תודה על הזמן שלך!
צוות {company_name}
```

## Social Media Templates

### Public Response to Complaint (Facebook/Instagram)

```
שלום {customer_name},
תודה שפנית אלינו. אנחנו מצטערים לשמוע על חוויית השירות שלך.
שלחנו לך הודעה פרטית כדי לטפל בנושא. נשמח לפתור את העניין בהקדם.
צוות {company_name}
```

### Private Follow-Up After Public Complaint

```
שלום {customer_name},

ראינו את הפנייה שלך ואנחנו רוצים לטפל בנושא.

כדי שנוכל לעזור, נשמח לקבל:
1. מספר הזמנה או מספר לקוח
2. תיאור קצר של הבעיה
3. דרך ליצור איתך קשר (טלפון / אימייל)

נטפל בפנייתך בעדיפות גבוהה.

בברכה,
{agent_name}
צוות שירות הלקוחות, {company_name}
```
