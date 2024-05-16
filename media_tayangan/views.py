from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
import uuid

# Create your views here.
def trailer_view(request):
    trailer_data = query(
        f"""WITH Views AS (
            SELECT
                rn.id_tayangan,
                COUNT(*) AS total_views
            FROM
                "PacilFlix"."RIWAYAT_NONTON" rn
            JOIN
                "PacilFlix"."FILM" f ON rn.id_tayangan = f.id_tayangan
            WHERE
                rn.end_date_time >= NOW() - INTERVAL '7 days' AND
                (rn.end_date_time - rn.start_date_time) >= INTERVAL '1 minute' * (f.durasi_film * 0.7)
            GROUP BY
                rn.id_tayangan
            UNION ALL
            SELECT
                rn.id_tayangan,
                COUNT(*) AS total_views
            FROM
                "PacilFlix"."RIWAYAT_NONTON" rn
            JOIN
                "PacilFlix"."EPISODE" e ON rn.id_tayangan = e.id_series
            WHERE
                rn.end_date_time >= NOW() - INTERVAL '7 days' AND
                (rn.end_date_time - rn.start_date_time) >= INTERVAL '1 minute' * (e.durasi * 0.7)
            GROUP BY
                rn.id_tayangan
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY total_views ASC) AS rank,
            t.judul,
            t.sinopsis_trailer,
            t.url_video_trailer,
            t.release_date_trailer,
            COALESCE(v.total_views, 0) AS total_views
        FROM
            "PacilFlix"."TAYANGAN" t
        LEFT JOIN
            Views v ON t.id = v.id_tayangan
        WHERE
            total_views > 0
        ORDER BY
            total_views DESC
        LIMIT 10;
        """
    )

    film_data = query(
        f'''WITH Views AS (
            SELECT
                rn.id_tayangan,
                COUNT(*) AS total_views
            FROM
                "PacilFlix"."RIWAYAT_NONTON" rn
            JOIN
                "PacilFlix"."FILM" f ON rn.id_tayangan = f.id_tayangan
            WHERE
                rn.end_date_time >= NOW() - INTERVAL '7 days' AND
                (rn.end_date_time - rn.start_date_time) >= INTERVAL '1 minute' * (f.durasi_film * 0.7)
            GROUP BY
                rn.id_tayangan
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY total_views ASC) AS rank,
            t.judul,
            t.sinopsis_trailer,
            t.url_video_trailer,
            t.release_date_trailer,
            COALESCE(v.total_views, 0) AS total_views
        FROM
            "PacilFlix"."TAYANGAN" t
        LEFT JOIN
            Views v ON t.id = v.id_tayangan
        JOIN 
            "PacilFlix"."FILM" film ON t.id = film.id_tayangan
        WHERE
            v.total_views > 0
        ORDER BY
            total_views DESC;
        '''
    )

    series_data = query(
        f'''WITH Views AS (
            SELECT
                rn.id_tayangan,
                COUNT(*) AS total_views
            FROM
                "PacilFlix"."RIWAYAT_NONTON" rn
            JOIN
                "PacilFlix"."EPISODE" e ON rn.id_tayangan = e.id_series
            WHERE
                rn.end_date_time >= NOW() - INTERVAL '7 days' AND
                (rn.end_date_time - rn.start_date_time) >= INTERVAL '1 minute' * (e.durasi * 0.7)
            GROUP BY
                rn.id_tayangan
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY total_views ASC) AS rank,
            t.judul,
            t.sinopsis_trailer,
            t.url_video_trailer,
            t.release_date_trailer,
            COALESCE(v.total_views, 0) AS total_views
        FROM
            "PacilFlix"."TAYANGAN" t
        LEFT JOIN
            Views v ON t.id = v.id_tayangan
        JOIN 
            "PacilFlix"."SERIES" series ON t.id = series.id_tayangan
        WHERE
            v.total_views > 0
        ORDER BY
            total_views DESC;
        '''
    )

    context = {
        "trailer_data": trailer_data,
        "film_data": film_data,
        "series_data": series_data,
    }
    
    return render(request, 'trailer.html', context)

def cari_trailer(request):
    return render(request, 'pencarian_trailer.html')

def tayangan_view(request):
    return render(request, 'tayangan.html')

def cari_tayangan(request):
    return render(request, 'pencarian_tayangan.html')

def film_view(request):
    return render(request, 'halaman_film.html')

def series_view(request):
    return render(request, 'halaman_series.html')

def episode_view(request):
    return render(request, 'halaman_episode.html')