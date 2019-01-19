<pre>
run:
./watershed.py <scieżka do obrazka png> -t <ścieżka do odpowiedniego ground truth>
./contour_following.py <scieżka do obrazka png> -t <ścieżka do odpowiedniego ground truth> -T <wartość progu> -a <minimalne pole powierzchni zmiany chorobowej> -A <maksymalne pole powierzchni>
minimalne pole powierzchni to ok. 30-60, maksymalne 300-500, wartość progu około 135 daje najlepsze wyniki (można zadać od 0 do 255)


input_dicom -> folder z DICOMami do segmentacji dla watershed.py
input_png -> folder ze skanami w png do segmentacji dla contour_following.py
ground_truths -> ręcznie posegmentowane skany do testowania jakości klasyfikacji
contour_results -> wyniki segmentacji metody countour w png
watershed_results -> wyniki segmentacji algorytmem segmentacji wododziałowej w png
contour_results.csv -> jakość segmentacji dla poszczególnych skanów segmentacji (alg. contour)
watershed_results.csv -> jakość segmentacji dla poszczególnych skanów segmentacji wododziałowej 
contour_following.py -> skrypt z algorytmem progowania z pomiarem pola powierzchni
watershed.py -> skrypt z algorytmem segmentacji wododziałowej
results.ods -> (openoffice calc/excel) ostateczne wyniki i średnie
</pre>
