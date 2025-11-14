
# Tableau Instructions – Full Workflow Guide

This guide covers:

1. Importing the cleaned CSV
2. Switching Data Source from **LIVE → EXTRACT**
3. Creating required visualizations
4. Exporting `.twbx`, `.tds`, `.hyper`
5. Using the generated .tds & .twb templates
6. Creating interactive Excel PivotTables locally

---

## 1. Import the Cleaned CSV into Tableau
1. Open **Tableau Desktop**
2. Click **Connect → Text File**
3. Load the file:
   ```
   cleaned_tableau_input.csv
   ```
4. Confirm the columns appear correctly.

---

## 2. Switch from LIVE to EXTRACT
1. Go to **Data** (top menu)
2. Click **Use Extract**
3. Tableau will prompt to create an extract → Click **OK**
4. Tableau generates:  
   ```
   Extract.hyper
   ```

This makes performance faster and allows exporting `.hyper`.

---

## 3. Build Required Visualizations

### A. Sales by Category (Bar)
- Drag **Category → Columns**
- Drag **Sales → Rows**
- Change Marks to **Bar**
- Sort descending

### B. Sales Trend (Line)
- Drag **Order Date → Columns**
- Change to **MONTH**
- Drag **Sales → Rows**
- Change Marks to **Line**

### C. Sales by Region (Map)
- Drag **Region → Canvas**
- Drag **Sales → Color**
- Choose **Filled Map**

---

## 4. Export Tableau Files

### A. Export `.twbx`
1. File → Save As
2. Choose **Tableau Packaged Workbook (.twbx)**  
Includes data + workbook.

### B. Export `.tds` (Tableau Data Source)
1. Right-click Data Source
2. Select **Add to Saved Data Sources**
3. Save as `.tds`

### C. Export `.hyper`
If extract is used, Tableau already created it automatically:
```
Documents/Tableau/Extracts/
```

---

## 5. Provided Template Files

### Included:
- **cleaned_data_source.tds** → Pre-linked data source
- **template_workbook.twb** → Workbook template (blank)

When opening `.twb`, Tableau may ask to locate the CSV → select `cleaned_tableau_input.csv`.

---

## 6. Interactive Excel Pivot Table (LOCAL MACHINE)

This environment cannot create Excel PivotTables (Excel feature is not supported here).

However, you already received:
```
generate_interactive_pivot_local.py
```

### To use it:
1. Copy **cleaned_tableau_input.csv** and the script to your laptop
2. Install:
   ```
   pip install xlsxwriter>=3.0
   ```
3. Run:
   ```
   python generate_interactive_pivot_local.py
   ```
4. It will generate:
   ```
   interactive_pivot_tables.xlsx
   ```
With a TRUE Excel Pivot Table (expand/collapse, drag fields, etc.).

---

Done!
