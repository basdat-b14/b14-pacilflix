from django.shortcuts import render


from utils.query import query
# Create your views here.
def trailer_view(request):
    #TODO: haven't checked series count
    trailer_data = query(
        f"""WITH EpisodeDurations AS (
                SELECT
                    e.id_series,
                    SUM(e.durasi) AS total_series_duration
                FROM
                    "PacilFlix"."EPISODE" e
                GROUP BY
                    e.id_series
            ),
            Views AS (
                SELECT
                    rn.id_tayangan,
                    COUNT(*) FILTER (WHERE f.id_tayangan IS NOT NULL AND (rn.end_date_time - rn.start_date_time) >= INTERVAL '1 minute' * (f.durasi_film * 0.7)) AS film_views,
                    COUNT(*) FILTER (WHERE e.id_series IS NOT NULL) AS episode_views,
                    SUM(EXTRACT(MINUTE FROM (rn.end_date_time - rn.start_date_time))) AS total_duration_watched
                FROM
                    "PacilFlix"."RIWAYAT_NONTON" rn
                LEFT JOIN
                    "PacilFlix"."FILM" f ON rn.id_tayangan = f.id_tayangan
                LEFT JOIN
                    "PacilFlix"."EPISODE" e ON rn.id_tayangan = e.id_series
                WHERE
                    rn.end_date_time >= NOW() - INTERVAL '7 days'
                GROUP BY
                    rn.id_tayangan, rn.username
            ),
            SeriesViews AS (
                SELECT
                    v.id_tayangan,
                    COUNT(*) AS total_views
                FROM
                    Views v
                LEFT JOIN
                    EpisodeDurations ed ON v.id_tayangan = ed.id_series
                WHERE
                    v.total_duration_watched >= (ed.total_series_duration * 0.7)
                    OR v.film_views > 0
                GROUP BY
                    v.id_tayangan
            )
            SELECT
                ROW_NUMBER() OVER (ORDER BY total_views ASC) AS rank,
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer,
                COALESCE(sv.total_views, 0) AS total_views
            FROM
                "PacilFlix"."TAYANGAN" t
            LEFT JOIN
                SeriesViews sv ON t.id = sv.id_tayangan
            ORDER BY
                total_views DESC
            LIMIT 10;
        """
    )

    film_data = query(
        f'''SELECT
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer
            FROM
                "PacilFlix"."TAYANGAN" t
            JOIN 
                "PacilFlix"."FILM" film ON t.id = film.id_tayangan;
        '''
    )

    series_data = query(
        f'''SELECT
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer
            FROM
                "PacilFlix"."TAYANGAN" t
            JOIN 
                "PacilFlix"."SERIES" series ON t.id = series.id_tayangan;
        '''
    )

    context = {
        "trailer_data": trailer_data,
        "film_data": film_data,
        "series_data": series_data,
    }
    
    return render(request, 'trailer.html', context)

def cari_trailer(request):
    judul_tayangan = request.GET.get('judul_tayangan')

    if judul_tayangan:
        tayangan = query(
            f'''SELECT
                    t.judul,
                    t.sinopsis_trailer,
                    t.url_video_trailer,
                    t.release_date_trailer
                FROM
                    "PacilFlix"."TAYANGAN" t
                WHERE
                    LOWER(t.judul) ILIKE LOWER('%{judul_tayangan}%');
            '''
        )
    else:
        tayangan = []
    
    context = {
        "tayangan": tayangan
    }

    return render(request, 'pencarian_trailer.html', context)

def tayangan_view(request):
    #TODO: haven't checked series count
    tayangan_data = query(
        f"""WITH EpisodeDurations AS (
                SELECT
                    e.id_series,
                    SUM(e.durasi) AS total_series_duration
                FROM
                    "PacilFlix"."EPISODE" e
                GROUP BY
                    e.id_series
            ),
            Views AS (
                SELECT
                    rn.id_tayangan,
                    COUNT(*) FILTER (WHERE f.id_tayangan IS NOT NULL AND (rn.end_date_time - rn.start_date_time) >= INTERVAL '1 minute' * (f.durasi_film * 0.7)) AS film_views,
                    COUNT(*) FILTER (WHERE e.id_series IS NOT NULL) AS episode_views,
                    SUM(EXTRACT(MINUTE FROM (rn.end_date_time - rn.start_date_time))) AS total_duration_watched
                FROM
                    "PacilFlix"."RIWAYAT_NONTON" rn
                LEFT JOIN
                    "PacilFlix"."FILM" f ON rn.id_tayangan = f.id_tayangan
                LEFT JOIN
                    "PacilFlix"."EPISODE" e ON rn.id_tayangan = e.id_series
                WHERE
                    rn.end_date_time >= NOW() - INTERVAL '7 days'
                GROUP BY
                    rn.id_tayangan, rn.username
            ),
            SeriesViews AS (
                SELECT
                    v.id_tayangan,
                    COUNT(*) AS total_views
                FROM
                    Views v
                LEFT JOIN
                    EpisodeDurations ed ON v.id_tayangan = ed.id_series
                WHERE
                    v.total_duration_watched >= (ed.total_series_duration * 0.7)
                    OR v.film_views > 0
                GROUP BY
                    v.id_tayangan
            )
            SELECT
                ROW_NUMBER() OVER (ORDER BY total_views ASC) AS rank,
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer,
                CASE
                    WHEN s.id_tayangan IS NOT NULL THEN 'series'
                    WHEN f.id_tayangan IS NOT NULL THEN 'film'
                    ELSE NULL
                END AS type,
                COALESCE(sv.total_views, 0) AS total_views
                FROM
                    "PacilFlix"."TAYANGAN" t
                LEFT JOIN
                    SeriesViews sv ON t.id = sv.id_tayangan
                LEFT JOIN
                    "PacilFlix"."SERIES" s ON t.id = s.id_tayangan
                LEFT JOIN
                    "PacilFlix"."FILM" f ON t.id = f.id_tayangan
            ORDER BY
                total_views DESC
            LIMIT 10;
        """
    )

    film_data = query(
        f'''SELECT
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer
            FROM
                "PacilFlix"."TAYANGAN" t
            JOIN 
                "PacilFlix"."FILM" film ON t.id = film.id_tayangan;
        '''
    )

    series_data = query(
        f'''SELECT
                t.judul,
                t.sinopsis_trailer,
                t.url_video_trailer,
                t.release_date_trailer
            FROM
                "PacilFlix"."TAYANGAN" t
            JOIN 
                "PacilFlix"."SERIES" series ON t.id = series.id_tayangan;
        '''
    )

    context = {
        "tayangan_data": tayangan_data,
        "film_data": film_data,
        "series_data": series_data,
    }

    return render(request, 'tayangan.html', context)

def cari_tayangan(request):
    judul_tayangan = request.GET.get('judul_tayangan')

    if judul_tayangan:
        tayangan = query(
            f'''SELECT
                    t.judul,
                    t.sinopsis_trailer,
                    t.url_video_trailer,
                    t.release_date_trailer,
                    CASE
                        WHEN s.id_tayangan IS NOT NULL THEN 'series'
                        WHEN f.id_tayangan IS NOT NULL THEN 'film'
                        ELSE NULL
                    END AS type
                FROM
                    "PacilFlix"."TAYANGAN" t
                LEFT JOIN
                    "PacilFlix"."SERIES" s ON t.id = s.id_tayangan
                LEFT JOIN
                    "PacilFlix"."FILM" f ON t.id = f.id_tayangan
                WHERE
                    LOWER(t.judul) ILIKE LOWER('%{judul_tayangan}%');
            '''
        )
    else:
        tayangan = []
    
    context = {
        "tayangan": tayangan
    }

    return render(request, 'pencarian_tayangan.html', context)

def film_view(request, judul):
    return render(request, 'halaman_film.html')

def series_view(request, judul):
    return render(request, 'halaman_series.html')

def episode_view(request):
    return render(request, 'halaman_episode.html')