from django.shortcuts import render, redirect
from utils.query import query, query_insert

def is_authenticated(request):
    try:
        request.session.get('username')
        return True
    except KeyError:
        return False
      
def trailer_view(request):
    trailer_data = query(
        """WITH EpisodeDurations AS (
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
        '''SELECT
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
        '''SELECT
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

#TODO: Sistem menampilkan [Tombol Halaman Tayangan] ketika pengguna memiliki paket aktif.
#Bila tidak, sistem tidak menampilkan tombol tersebut.

def tayangan_view(request):
    if not is_authenticated(request):
        return redirect('/login')
    
    # check_package = query(
    #     f"""SELECT
    #         CASE
    #             WHEN MAX(t.end_date_time) > current_date THEN 1
    #             ELSE 0
    #         END AS is_active
    #         FROM
    #         "PacilFlix"."TRANSACTIONS" t
    #         JOIN "PacilFlix"."PENGGUNA" p ON t.username = p.username
    #         WHERE
    #         p.username = '{request.session.get('username')}'
    #     """
    # )
    
    tayangan_data = query(
        """WITH EpisodeDurations AS (
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
        '''SELECT
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
        '''SELECT
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
        # "check_package": check_package,
        "tayangan_data": tayangan_data,
        "film_data": film_data,
        "series_data": series_data,
    }

    return render(request, 'tayangan.html', context)

def cari_tayangan(request):
    if not is_authenticated(request):
        return redirect('/login')
    
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
    if not is_authenticated(request):
        return redirect('/login')
    
    film_data = query(
        f'''SELECT
                t.judul,
                count(r.username) as "total_view",
                round(avg(u.rating), 1) as "rating",
                t.sinopsis,
                f.durasi_film,
                f.release_date_film,
                f.url_video_film,
                array_to_string(array_agg(DISTINCT gt.genre), ',') AS "genre",
                t.asal_negara,
                array_to_string(array_agg(DISTINCT pc.nama ORDER BY pc.nama), ',') AS "pemain",
                array_to_string(array_agg(DISTINCT ps.nama ORDER BY ps.nama), ',') AS "penulis",
                array_to_string(array_agg(DISTINCT d.nama ORDER BY d.nama), ',') AS "sutradara",
                CASE
                    WHEN f.release_date_film <= current_date THEN 'Released'
                    ELSE 'Not Released'
                END AS "status"
            FROM
                "PacilFlix"."TAYANGAN" as t
                JOIN "PacilFlix"."FILM" as f ON t.id = f.id_tayangan
                LEFT JOIN "PacilFlix"."RIWAYAT_NONTON" as r ON t.id = r.id_tayangan
                LEFT JOIN "PacilFlix"."ULASAN" as u ON t.id = u.id_tayangan
                LEFT JOIN "PacilFlix"."GENRE_TAYANGAN" as gt ON t.id = gt.id_tayangan
                LEFT JOIN "PacilFlix"."MEMAINKAN_TAYANGAN" as mt ON t.id = mt.id_tayangan
                LEFT JOIN "PacilFlix"."CONTRIBUTORS" as pc ON mt.id_pemain = pc.id
                LEFT JOIN "PacilFlix"."MENULIS_SKENARIO_TAYANGAN" as mst ON t.id = mst.id_tayangan
                LEFT JOIN "PacilFlix"."CONTRIBUTORS" as ps ON mst.id_penulis_skenario = ps.id
                LEFT JOIN "PacilFlix"."SUTRADARA" AS s ON t.id_sutradara = s.id
                LEFT JOIN "PacilFlix"."CONTRIBUTORS" AS d ON s.id = d.id
            WHERE
                t.judul = '{judul}'
            GROUP BY
                t.id, f.durasi_film, f.release_date_film, f.url_video_film;
        '''
    )

    review_data = query(
        f'''SELECT
                u.username,
                u.rating,
                u.deskripsi
            FROM
                "PacilFlix"."ULASAN" AS u
            JOIN
                "PacilFlix"."TAYANGAN" AS t ON u.id_tayangan = t.id
            WHERE
                t.judul = '{judul}'
            ORDER BY
                u.timestamp DESC;
        '''
    )

    penulis_list = []
    pemain_list = []

    penulis_list.extend(film_data[0].penulis.split(','))
    pemain_list.extend(film_data[0].pemain.split(','))

    context = {
        "film_data": film_data,
        "penulis_list": penulis_list,
        "pemain_list": pemain_list,
        "review_data": review_data
    }

    return render(request, 'halaman_film.html', context)

def series_view(request, judul):
    if not is_authenticated(request):
        return redirect('/login')
    
    series_data = query(
        f'''SELECT
                t.judul,
                count(r.username) as "total_view",
                round(avg(u.rating), 1) as "rating",
                t.sinopsis,
                array_to_string(array_agg(DISTINCT gt.genre), ',') AS "genre",
                t.asal_negara,
                array_to_string(array_agg(DISTINCT pc.nama ORDER BY pc.nama), ',') AS "pemain",
                array_to_string(array_agg(DISTINCT ps.nama ORDER BY ps.nama), ',') AS "penulis",
                array_to_string(array_agg(DISTINCT d.nama ORDER BY d.nama), ',') AS "sutradara",
                array_to_string(array_agg(DISTINCT e.sub_judul), ',') AS "episode"
            FROM
                "PacilFlix"."TAYANGAN" as t
            JOIN "PacilFlix"."SERIES" as se ON t.id = se.id_tayangan
            LEFT JOIN (
                SELECT
                id_series,
                array_agg(sub_judul) as sub_judul
                FROM
                "PacilFlix"."EPISODE"
                GROUP BY
                id_series
            ) AS e ON se.id_tayangan = e.id_series
            LEFT JOIN "PacilFlix"."RIWAYAT_NONTON" as r ON t.id = r.id_tayangan
            LEFT JOIN "PacilFlix"."ULASAN" as u ON t.id = u.id_tayangan
            LEFT JOIN "PacilFlix"."GENRE_TAYANGAN" as gt ON t.id = gt.id_tayangan
            LEFT JOIN "PacilFlix"."MEMAINKAN_TAYANGAN" as mt ON t.id = mt.id_tayangan
            LEFT JOIN "PacilFlix"."CONTRIBUTORS" as pc ON mt.id_pemain = pc.id
            LEFT JOIN "PacilFlix"."MENULIS_SKENARIO_TAYANGAN" as mst ON t.id = mst.id_tayangan
            LEFT JOIN "PacilFlix"."CONTRIBUTORS" as ps ON mst.id_penulis_skenario = ps.id
            LEFT JOIN "PacilFlix"."SUTRADARA" AS s ON t.id_sutradara = s.id
            LEFT JOIN "PacilFlix"."CONTRIBUTORS" AS d ON s.id = d.id
            WHERE
                t.judul = '{judul}'
            GROUP BY
                t.id;
        '''
    )

    review_data = query(
        f'''SELECT
                u.username,
                u.rating,
                u.deskripsi
            FROM
                "PacilFlix"."ULASAN" AS u
            JOIN
                "PacilFlix"."TAYANGAN" AS t ON u.id_tayangan = t.id
            WHERE
                t.judul = '{judul}'
            ORDER BY
                u.timestamp DESC;
        '''
    )

    penulis_list = []
    pemain_list = []
    episode_list = []

    penulis_list.extend(series_data[0].penulis.split(','))
    pemain_list.extend(series_data[0].pemain.split(','))
    episode_list.extend(series_data[0].episode.split(','))

    context = {
        "series_data": series_data,
        "penulis_list": penulis_list,
        "pemain_list": pemain_list,
        "episode_list": episode_list,
        "review_data": review_data
    }

    return render(request, 'halaman_series.html', context)

def episode_view(request, judul):
    if not is_authenticated(request):
        return redirect('/login')
    
    episode_data = query(
        f'''SELECT
                t.judul,
                e.sub_judul,
                e.sinopsis,
                e.durasi,
                e.url_video,
                e.release_date
            FROM
                "PacilFlix"."TAYANGAN" AS t
            JOIN "PacilFlix"."SERIES" AS se ON t.id = se.id_tayangan
            JOIN "PacilFlix"."EPISODE" AS e ON se.id_tayangan = e.id_series
            WHERE
                e.sub_judul = '{judul}'
            GROUP BY
                t.judul, e.sub_judul, e.sinopsis, e.durasi, e.url_video, e.release_date;
        '''
    )

    other_episode = query(
        f'''SELECT
                e.sub_judul
            FROM
                "PacilFlix"."EPISODE" AS e
            JOIN "PacilFlix"."SERIES" AS se ON e.id_series = se.id_tayangan
            JOIN "PacilFlix"."TAYANGAN" AS t ON se.id_tayangan = t.id
            WHERE
                se.id_tayangan = (
                    SELECT
                        sr.id_tayangan
                    FROM
                        "PacilFlix"."EPISODE" AS ep
                    JOIN "PacilFlix"."SERIES" AS sr ON ep.id_series = sr.id_tayangan
                    WHERE
                        ep.sub_judul = '{judul}'
                )
            AND e.sub_judul != '{judul}';
        '''
    )

    other_episode_list = []

    for episode in other_episode:
        other_episode_list.extend(episode)

    context = {
        "episode_data": episode_data,
        "other_episode_list": other_episode_list
    }

    return render(request, 'halaman_episode.html', context)

def save_progress_series(request):
    if not is_authenticated(request):
        return redirect('/login')
    
    if request.method == 'POST':
        judul = request.POST.get('judul')
        progress = request.POST.get('progress')
        username = request.session.get('username')

        if judul and progress and username:
            query_insert(f'''
                INSERT INTO "PacilFlix"."RIWAYAT_NONTON" (id_tayangan, username, start_date_time, end_date_time)
                VALUES (
                    (SELECT
                        t.id
                    FROM
                        "PacilFlix"."TAYANGAN" AS t
                    JOIN "PacilFlix"."SERIES" AS se ON t.id = se.id_tayangan
                    JOIN "PacilFlix"."EPISODE" AS e ON se.id_tayangan = e.id_series
                    WHERE
                        e.sub_judul = '{judul}'
                    ),
                    '{username}',
                    DATE_TRUNC('second', current_timestamp),
                    DATE_TRUNC('second', current_timestamp + interval '{progress} minute')
                );
            ''')

    return redirect('episode_view', judul=judul)
    
def save_progress_film(request):
    if not is_authenticated(request):
        return redirect('/login')
    
    if request.method == 'POST':
        judul = request.POST.get('judul')
        progress = request.POST.get('progress')
        username = request.session.get('username')

        if judul and progress and username:
            query_insert(f'''
                INSERT INTO "PacilFlix"."RIWAYAT_NONTON" (id_tayangan, username, start_date_time, end_date_time)
                VALUES (
                    (SELECT
                        t.id
                    FROM
                        "PacilFlix"."TAYANGAN" AS t
                    WHERE
                        t.judul = '{judul}'
                    ),
                    '{username}',
                    DATE_TRUNC('second', current_timestamp),
                    DATE_TRUNC('second', current_timestamp + interval '{progress} minute')
                );
            ''')

    return redirect('film_view', judul=judul)
    
def ulasan(request):
    if not is_authenticated(request):
        return redirect('/login')
    
    if request.method == 'POST':
        judul = request.POST.get('judul')
        rating = request.POST.get('rating')
        deskripsi = request.POST.get('deskripsi')
        username = request.session.get('username')

        print(username, judul, rating, deskripsi)

        if judul and rating and deskripsi and username:
            query_insert(f'''
                INSERT INTO "PacilFlix"."ULASAN" (id_tayangan, timestamp, username, rating, deskripsi)
                VALUES (
                    (SELECT
                        t.id
                    FROM
                        "PacilFlix"."TAYANGAN" AS t
                    WHERE
                        t.judul = '{judul}'
                    ),
                    DATE_TRUNC('second', current_timestamp),
                    '{username}',
                    {rating},
                    '{deskripsi}'
                );
            ''')


        tayangan_type = query(
            f'''SELECT
                CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM "PacilFlix"."SERIES"
                    WHERE id_tayangan = (
                    SELECT id
                    FROM "PacilFlix"."TAYANGAN"
                    WHERE judul = '{judul}'
                    )
                ) THEN 'series'
                ELSE 'film'
                END AS tayangan_type;
            '''
        )

    if tayangan_type[0].tayangan_type == 'series':
        return redirect('series_view', judul=judul)
    else:
        return redirect('film_view', judul=judul)