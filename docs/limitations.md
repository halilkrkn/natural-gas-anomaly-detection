# Tez sınırlılıkları — kayıtlı yöntem notları

## Zaman-temelli erken uyarı etiketi

Kademeli senaryoda 6–12 saat aralığı zamana göre `early_warning` olarak etiketlenir; ancak rampanın başında sızıntı sinyali ölçüm gürültüsü seviyesinin altında kalabilir. Bu nedenle Early sınıfının recall değerinin düşük çıkması beklenebilir. Sonuçlar sınıf bazında raporlanacak ve bu durum, tek başına yöntem hatası olarak değil, zaman-temelli etiketleme yaklaşımının bir sonucu olarak tartışılacaktır. Lead time (`t_critical - t_detect`) bu sınıf etiketinden bağımsız hesaplanır.

## Sentetik veri ve fiziksel model kapsamı

Sentetik koşular aynı quasi-steady-state Weymouth üreticisi ve basit periyodik talep profiliyle üretildiğinden, sonuçlar bu kontrollü üretici altındaki yöntem karşılaştırmasını gösterir; gerçek doğal gaz iletim şebekelerine doğrudan genellenebilirlik iddiası taşımaz. Model, geçici rejim PDE/CFD veya gerçek işletme verisi doğrulaması değildir.

## Post-faz ve pencere dışlama varsayımı

Kademeli sızıntı 18. saatte sonlandırılır; sensör drift enjeksiyonu da aynı anda kaldırılarak offset sıfırlanır. Quasi-steady v1 modeli geçici basınç/debi toparlanmasını simüle etmez; normal duruma dönüş anlık kabul edilir. W=16 penceresinde reset öncesi anomali gözlemleri kalabileceğinden, 16 ardışık post-reset örnek oluşana kadar bu geçiş pencereleri üç sınıflı kalibrasyon ve sınıf-metriği hesaplarından dışlanır. Bu dışlama kuralı fiziksel toparlanma dinamiğini temsil etmez; pencere geçmişinin etiketle çelişmesini azaltan yöntemsel bir tercihtir.
