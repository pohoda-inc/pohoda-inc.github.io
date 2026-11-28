#!/usr/bin/env python3
"""法人向け SaaS の LP（one-crm.html・katachi-plus.html、のちに one-inventory.html）を作る。

型は assets/saas.css。中身は下の PRODUCTS に書き、ページはここから作り直す（手で直さない）。
ヘッダーとフッターは、今あるページのものをそのまま使う（サイト共通の部品の変更に追従するため）。

  python3 tools/saas_lp.py            # 全部
  python3 tools/saas_lp.py one-crm    # 1本だけ

料金を変えたら PRODUCTS の price と、特商法・llms.txt・business.html も直す。
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAIL = 'pohoda.inc@gmail.com'


def yen(n):
    return f'¥{n:,}'


ONE_CRM = dict(
    slug='one-crm', name='One CRM', app_id='6813791048', ct='pj-one-crm', icon='onecrm-icon.png',
    title='One CRM｜小さな会社・個人事業主の顧客管理（料金・機能・比較）',
    description='One CRM は、顧客と会ったことを記録するだけで最後に連絡した日・回数・売上が自動で出る顧客管理。iPhone・iPad・Mac で使え、チームで共有できます。顧客10件まで無料、Pro は使う人1人ごとに買い切り980円（税込）。データは自分の iCloud に保存。',
    og_title='One CRM｜顧客・商談・案件を、ひとつの台帳に。',
    og_description='最後に連絡した日も売上も自動で計算。チームで共有でき、データは自分の iCloud に。',
    ld_description='小さな会社・個人事業主の顧客管理。最後に連絡した日・回数・売上を自動計算。チームで共有でき、データは自分の iCloud に保存。',
    free_offer='無料（顧客10件まで）',
    price=dict(life=980),
    kind='小さな会社と個人事業主の顧客管理',
    h1='顧客・商談・案件を、<br>ひとつの台帳に。',
    lead='会ったことを記録するだけで、最後に連絡した日・回数・売上が自動で出ます。iPhone・iPad・Mac で同じ台帳を使い、チームで共有できます。顧客のデータは Pohoda のサーバーを通らず、自分の iCloud に置かれます。',
    assure='顧客10件まで無料・カードの登録なし・アカウント登録なし',
    hero_mac=('onecrm-mac-01-three-columns.jpg', 1880, 957, 'Mac の One CRM。左に顧客の一覧、右に選んだ顧客の最終来店・今月の売上・来店回数とこれまでの記録'),
    hero_phone=('onecrm-iphone-home.jpg', 405, 880, 'iPhone の One CRM のホーム'),
    solve_title='紙やエクセルの顧客管理で、止まりがちなこと',
    solve=[
        ('「あの人、最後に会ったのいつだっけ」', '最後に連絡した日が、自動で出る', '会った日を記録するだけで、最後に連絡した日・回数・今月の売上・累計が顧客ごとに出ます。しばらく連絡していない人はホームに並びます。'),
        ('「外の会社に顧客の情報を預けたくない」', 'データは自分の iCloud に', 'Pohoda はサーバーを持たないので、顧客のデータを受け取ることも見ることもできません。端末と、ご自身の iCloud にだけ置かれます。'),
        ('「数人の会社には、大きな CRM は高い」', '1人980円の買い切りだけ', '料金は使う人1人ごとに、980円を一度だけ。毎月の費用はかからず、何人で使っても増えるのは人数分だけです。'),
    ],
    kinds_title='商売の形に合わせた型から始める',
    kinds_intro='最初に型を選ぶと、項目と呼び名がその形に合わせて入ります。あとから自由に作り替えられます。',
    kinds=[
        ('法人営業', '営業代行・士業・制作会社・BtoB の営業', '取引先に担当者を何人でも紐付け、案件を「案件化→見積提示→受注」のような段階で管理します。', 'anken-kanrihyo-template.html', '案件管理表のテンプレート'),
        ('接客・サロン', '美容室・サロン・教室・施術', '来店ごとの記録と売上、次の予約。よく来る人から選ぶだけで、日付の入った記録が開きます。', 'salon-counseling-sheet-template.html', 'カウンセリングシートのテンプレート'),
        ('物販・ハンドメイド', 'ネットショップ・イベント出店・個人の店', 'お客さまごとの注文と金額、リピートの回数。誰がいつ何を買ったかを一つの台帳で追えます。', 'kokyaku-daicho-template.html', '顧客台帳のテンプレート'),
    ],
    feats_intro='顧客の台帳と、会ったことの記録に絞っています。<span class="pro">Pro</span> の印があるものは Pro で使えます。',
    rows=[
        ('顧客ごとの数字が、記録から自動で', '一覧で最後に会った日・回数・累計の売上が並び、選ぶとこれまでの記録が日付順に出ます。',
         ['最後に連絡した日・回数・今月の売上・累計を自動で計算', '状況・タグ・最終来店で絞り込みと並べ替え', '顧客ごとの分析<span class="pro">Pro</span>'],
         ('onecrm-mac-01-three-columns.jpg', 1880, 957, '顧客の一覧と、選んだ顧客の記録')),
        ('記録は、選んで金額を入れるだけ', 'よく来る人がボタンで並び、日付と時刻は入った状態で開きます。対応する iPhone では、話した言葉から記録の下書きも作れます（端末の中で処理）。',
         ['来店・案件・タスク・ノートをその場で追加', '予約や次の連絡の通知', 'しばらく連絡していない顧客・止まった案件がホームに並ぶ'],
         ('onecrm-mac-02-quicklog.jpg', 1880, 957, '来店を記録する画面。顧客を選び、金額とメモを入れて保存する')),
        ('項目も呼び名も、自社のやり方に', '顧客・来店・案件などの「コレクション」と、その中の項目を自由に足せます。案件の段階の選択肢も作り替えられます。',
         ['金額・日付・選択・タグ・評価・写真などの項目', '事業ごとに台帳を分ける（行き来はいつでも）', 'Excel の CSV をそのまま取り込み'],
         ('onecrm-mac-03-customize.jpg', 1880, 957, 'カスタマイズの画面。事業・コレクション・iCloud 同期・バックアップの設定')),
    ],
    more=['メンバーを招待して同じ台帳を使う<span class="pro">Pro</span>', '参加した人を外す・共有をやめるのはオーナーだけ', 'iPhone・iPad・Mac で同じ内容に同期',
          'Face ID でアプリにロック', 'バックアップの書き出しと復元', 'CSV の書き出し（Excel で開ける）',
          '取引先に担当者を何人でも紐付け', 'ライト・ダークの表示', '広告・追跡なし'],
    pricing_intro='料金は買い切りだけです。チームで使うときは、オーナーも参加する人もそれぞれ Pro を一度だけ購入します。毎月・毎年の支払いはありません。',
    free_items=['顧客は全ビジネス合計で10件まで', '記録・通知・アプリロック', 'バックアップと CSV の書き出し・取り込み', 'iPhone・iPad・Mac で同期'],
    free_name='無料', pro_name='Pro', pro_btn='無料ではじめて、アプリから Pro に',
    life_sub='使う人それぞれ1回・以後の支払いなし・今後の機能も含む',
    pro_items=['顧客・コレクション・項目・自動計算の上限なし', 'チームで同じ台帳を使う（日本の App Store）', '顧客ごとの分析', '無料の機能はすべて含む'],
    price_note='価格は税込です。お支払いは App Store（Apple ID）で一度だけ、請求書払いはありません。すでに月額・年額で登録している方は、解約するまでそのまま使えます。詳しくは<a href="./legal/tokushoho.html">特定商取引法に基づく表記</a>へ。',
    compare_intro='大手のクラウド CRM（Salesforce・HubSpot など）と、表計算（Excel・スプレッドシート）で顧客を管理する場合と比べました。One CRM にないものも書いています。',
    compare_cols=['大手のクラウド CRM', '表計算'],
    compare=[
        ('料金の形', '10件まで無料。Pro は1人 買い切り980円（毎月の費用なし）', '1人ごとの月額が中心。無料の版があるものも', '表計算ソフトの料金だけ'),
        ('始めるまで', 'y|入れてすぐ。アカウント登録なし', '会社のアカウントを作り、初期設定をする', '列と関数を自分で作る'),
        ('スマホで記録', 'y|iPhone・iPad・Mac のアプリ', 'y|アプリあり', 'n|小さい画面では入力しにくい'),
        ('最後に連絡した日・売上の集計', 'y|記録するだけで自動', 'y|設定すれば出せる', 'n|関数を自分で組む'),
        ('チームで共有', 'y|招待した人だけ（日本・Pro）', 'y|できる。権限も細かく分けられる', 'y|ファイルの共有で'),
        ('データの置き場所', '端末と自分の iCloud', '提供会社のサーバー', '自分のパソコンかクラウドのドライブ'),
        ('メール配信・自動化・外部連携', 'n|ない', 'y|ある', 'n|ない'),
        ('ブラウザ・Android・Windows', 'n|使えない', 'y|使える', 'y|使える'),
    ],
    compare_note='大手のクラウド CRM の内容は一般的な傾向です。料金や機能は各社の公式サイトで確かめてください。iPhone の顧客管理アプリ6本との比較は<a href="./journal/kokyaku-kanri-app-erabikata.html">顧客管理アプリの選び方と比較</a>にあります。',
    where_intro='顧客の名前や連絡先は、預ける先が少ないほど漏れにくくなります。One CRM は Pohoda のサーバーを使いません。',
    where=[
        ('端末', '入力したデータは、まずこの iPhone・iPad・Mac に保存されます。Face ID でアプリにロックをかけられます。'),
        ('自分の iCloud', '同期がオンのとき、ご自身の Apple アカウントの iCloud に置かれ、ほかの端末と同じ内容になります。同期はオフにもできます。'),
        ('Pohoda のサーバー', 'ありません。データは送られず、Pohoda が見ることもできません。広告・追跡・アカウント登録もありません。'),
    ],
    where_note='チームで共有したデータは、オーナーの iCloud に置かれ、招待した人だけが読み書きできます。詳しくは<a href="./legal/privacy.html">プライバシーポリシー</a>へ。',
    steps_intro='営業の人との打ち合わせはありません。その日のうちに使い始められます。',
    steps=[
        ('アプリを入れる', 'App Store から入れて、商売の形（法人営業・接客・物販）を選びます。アカウント登録はありません。'),
        ('顧客を入れる', '手で足すか、Excel の顧客リストを CSV で取り込みます。10件までは無料で試せます。'),
        ('チームを招待する', '一緒に使う人がいれば、Pro にして「チームで使う」から招待を送ります。参加する人も Pro にします。'),
    ],
    guide='one-crm-guide.html',
    faq=[
        ('One CRM はどんなサービスですか？', '小さな会社や個人事業主のための顧客管理です。顧客の名前と会ったことを記録すると、最後に連絡した日・回数・今月の売上・累計が自動で出ます。iPhone・iPad・Mac のアプリで使い、チームで同じ台帳を共有できます。'),
        ('無料で使えますか？', 'はい。顧客は全ビジネス合計で10件まで無料です。記録・通知・バックアップ・CSV の書き出しと取り込み・アプリロックは無料のまま使えます。無料の間はカードの登録もありません。Pro にすると、登録件数や項目などの上限がなくなり、顧客ごとの分析とチームでの共有が使えます。'),
        ('チームで使うと、料金はどうなりますか？', 'オーナーも参加する人も、それぞれ Pro（買い切り980円）を一度だけ購入します。3人なら合計2,940円で、以後の支払いはありません。チームでの共有は日本の App Store で使えます。'),
        ('データはどこに保存されますか？', '端末と、ご自身の iCloud です（同期は初期設定でオン・オフにもできます）。Pohoda はサーバーを持たず、データを受け取ることも見ることもできません。アカウント登録も不要で、Face ID でロックをかけられます。'),
        ('エクセルや他の顧客管理から移せますか？', 'はい。CSV で取り込めます。Excel で保存した CSV をそのまま読め（UTF-8・Shift_JIS）、1行目の項目名と同じ名前の項目に自動で割り当てます。金額は「1,000」「¥1,000」「1000円」、日付は「2026/1/5」「2026年1月5日」なども読めます。'),
        ('請求書払いはできますか？', 'できません。お支払いは App Store（Apple ID）だけです。領収書は Apple から届くメールか、App Store の購入履歴から出せます。'),
        ('ブラウザや Android・Windows で使えますか？', '使えません。iPhone・iPad・Mac のアプリです。'),
        ('メール配信や、外部サービスとの連携はありますか？', 'ありません。One CRM は顧客と記録の台帳に絞っています。メールの一斉配信や営業の自動化が必要なら、大手のクラウド CRM が向いています。'),
    ],
    final_title='まずは10件、無料で試せます',
    final_foot='運営は Pohoda（杉本 啓輔・個人事業）。日本の事業者向けです。',
    reads=[
        ('kokyaku-kanri-app-erabikata.html', '顧客管理アプリの選び方と比較（2026）', '選び方'),
        ('anken-kanrihyo-template.html', '案件管理表のテンプレート（印刷用・無料）', 'テンプレート'),
        ('kokyaku-kanrihyo-excel.html', '顧客管理表のエクセルの作り方（印刷用シートつき）', 'テンプレート'),
        ('kokyaku-daicho-template.html', '顧客台帳のテンプレート（印刷用・無料）', 'テンプレート'),
        ('salon-counseling-sheet-template.html', '美容室のカウンセリングシート・顧客カルテのテンプレート', 'テンプレート'),
    ],
)

KATACHI_PLUS = dict(
    slug='katachi-plus', name='KATACHI +', app_id='6815231799', ct='pj-katachi-plus', icon='katachi-plus-icon.png',
    title='パーソナルジム・スタジオの顧客管理 KATACHI +｜カルテ・予約台帳・料金・比較',
    description='KATACHI + は、パーソナルトレーナーと小さなジム・スタジオの顧客カルテ・セッション記録・予約台帳・分析。スタッフを招待して店舗で共有でき、記録はオーナーの iCloud に保存。1人・顧客5人まで無料、使う人1人ごとに買い切り980円（税込）。',
    og_title='KATACHI +｜顧客カルテと予約台帳を、店舗のみんなで。',
    og_description='記録は Pohoda のサーバーを通らず、オーナーの iCloud に。スタッフを招待して店舗で共有。',
    ld_description='パーソナルトレーナーと小さなジム・スタジオの顧客カルテ・セッション記録・予約台帳・分析。スタッフと店舗で共有でき、記録はオーナーの iCloud に保存。',
    free_offer='無料（1人・顧客5人まで）',
    price=dict(life=980),
    kind='パーソナルジム・スタジオの顧客カルテと予約台帳',
    h1='顧客カルテと予約台帳を、<br>店舗のみんなで。',
    lead='パーソナルトレーナーと小さなジム・スタジオのための、顧客カルテ・セッション記録・予約台帳・分析。スタッフを招待して店舗で共有できます。顧客の記録は Pohoda のサーバーを通らず、オーナーの iCloud に置かれます。',
    assure='1人・顧客5人まで無料・カードの登録なし・アカウント登録なし',
    hero_mac=('katachi-plus-mac-karte.jpg', 1280, 800, 'Mac の KATACHI +。左に今日の予約と顧客の一覧、中央に指導方針と引き継ぎメモ、右にセッションの記録'),
    hero_phone=('katachi-plus-iphone.jpg', 405, 880, 'iPhone の KATACHI + の顧客一覧'),
    solve_title='紙のカルテと別々の道具で、止まりがちなこと',
    solve=[
        ('「担当が替わると、前回の内容が分からない」', 'カルテと申し送りを店舗で共有', '指導方針と引き継ぎメモがカルテのいちばん上に。前回の記録を見ながら、セットを数タップで足せます。'),
        ('「同意書とカウンセリングシートの紙が溜まる」', '同意書もカウンセリングも iPad で', '人体図をタップして気になる部位を記録。同意書はその場で署名してもらい、PDF で残ります。'),
        ('「予約システムは高く、記録は別のノート」', '1人980円の買い切りだけ', '予約の受付は今の LINE・電話・予約サービスのまま。受けた予約を台帳に入れ、そのままセッションの記録へ進めます。'),
    ],
    kinds_title='業種を選ぶと、記録の入力欄が変わる',
    kinds_intro='店舗を作るときに業種を選ぶと、種目・記録の入力欄・カウンセリングの質問がその業種に合わせて入ります。',
    kinds=[
        ('筋トレ', 'パーソナルジム', '重量×回数でセットを記録。推定最大重量とボリュームのグラフ、体組成の推移も見られます。', 'personal-training-karte-template.html', 'カルテのテンプレート'),
        ('ピラティス', 'ピラティススタジオ', 'マシン・スプリング・回数・左右を記録。姿勢の変化を写真で見比べられます。', 'pilates-studio-kokyaku-kanri-erabikata.html', 'ピラティススタジオの選び方と比較'),
        ('ヨガ', 'ヨガスタジオ・プライベートレッスン', 'ポーズごとの呼吸数・左右・バリエーションを記録します。', 'personal-gym-counseling-sheet.html', 'カウンセリングシートのテンプレート'),
        ('ストレッチ', 'ストレッチ専門店・整体', '保持時間・方法・強さを記録し、柔軟性を前後で比べられます。', 'trainer-kokyaku-kanri-app-erabikata.html', 'トレーナーの顧客管理の選び方'),
    ],
    feats_intro='カルテ・記録・予約台帳・分析をひとつに。<span class="pro">購入</span> の印があるものは、使う人ごとに買い切りを購入すると使えます。',
    rows=[
        ('カルテに、方針と申し送り', '顧客を選ぶと、指導方針・引き継ぎメモ・これまでのセッションが1画面に並びます。書いた人と日時が残り、店舗のスタッフ全員が見られます。',
         ['顧客台帳（顔写真・連絡先・生年月日・目的・担当・配慮事項）', 'カウンセリングシート（人体図をタップして部位を記録）', 'iPad でその場で署名する同意書（PDF で保存）'],
         ('katachi-plus-mac-karte.jpg', 1280, 800, '顧客のカルテ。指導方針と引き継ぎメモ、基本情報、セッションの一覧')),
        ('対面のセッションを、速く記録', '前回の重量と回数が出た状態で開き、セットは数タップで足せます。メニューの型から始められ、入力のたびに自動で保存します。',
         ['当日のコンディション（睡眠・疲労・きつさ）', '体重・体脂肪・周径の推移と、同じ向きで並べる姿勢写真', 'その日の記録と推移を PDF のレポートにして顧客に共有'],
         ('katachi-plus-mac-record.jpg', 1280, 800, 'セッションの記録。種目ごとに前回の値と、重量・回数のセット')),
        ('予約台帳から、そのまま記録へ', 'LINE や電話、予約サービスで受けた予約を、日・週で担当者ごとに確認します。予約からそのままセッションの記録へ進めます。',
         ['担当者での絞り込み', '実施済み・キャンセルの記録', '店舗の予約ページのリンクを登録して顧客に送れる'],
         ('katachi-plus-mac-yoyaku.jpg', 1280, 800, '予約台帳の週の表示。担当者ごとの予約と実施済み・キャンセル')),
        ('店舗と担当者の数字を、月ごとに', '顧客数・セッション数・予約数と実施率を、店舗全体と担当者ごとに見られます。',
         ['顧客数と新しく増えた人数の推移', '担当者ごとの顧客数とセッション数', '前月との比較'],
         ('katachi-plus-mac-bunseki.jpg', 1280, 800, '分析の画面。顧客数・セッション数の推移と担当者ごとの数字')),
    ],
    more=['スタッフを招待して店舗で共有<span class="pro">購入</span>', '退職したスタッフを外すと、その人の端末から店舗の記録が消える', '2つ目以降の店舗<span class="pro">購入</span>',
          'お客さまの KATACHI とつなぎ、自主練の記録を受け取る', 'CSV の書き出し', 'CSV の取り込み・バックアップの復元<span class="pro">購入</span>',
          '端末内の自動バックアップ（7世代）', 'Face ID・パスコードでアプリにロック', 'iPhone・iPad・Mac で使える'],
    pricing_intro='1人で使う分は無料です。顧客を6人以上記録する、スタッフを招待して店舗で共有するときは、使う人それぞれが買い切り（980円）を一度だけ購入します。店舗に参加するスタッフも、それぞれ必要です。',
    free_items=['自分の店舗1つで、顧客5人まで', 'セッション・予約・同意書・体組成・写真の記録', '顧客へのレポート・CSV の書き出し・バックアップ', 'お客さまの KATACHI との連携'],
    free_name='1人で使う', pro_name='顧客6人から・スタッフと共有', pro_btn='無料ではじめて、必要になったら購入',
    life_sub='使う人それぞれ1回・以後の支払いなし',
    pro_items=['顧客の人数の上限なし', 'スタッフの招待と、店舗への参加', '2つ目以降の店舗', 'CSV の取り込み・バックアップの復元'],
    price_note='価格は税込です。お支払いは App Store（Apple ID）で一度だけ、請求書払いはありません。すでに月額・年額で登録している方は、解約するまでそのまま使えます。詳しくは<a href="./legal/tokushoho.html">特定商取引法に基づく表記</a>・<a href="./legal/katachi-plus-terms.html">利用規約</a>へ。',
    compare_intro='予約・会員管理のシステム（hacomono・STORES 予約など）と、紙や表計算のカルテと比べました。KATACHI + にないものも書いています。',
    compare_cols=['予約・会員管理のシステム', '紙・表計算'],
    compare=[
        ('料金の形', '1人・顧客5人まで無料。1人 買い切り980円（毎月の費用なし）', '店舗ごとの月額が中心。初期費用がかかるものも', '紙代と表計算ソフトの料金だけ'),
        ('顧客が自分で予約', 'n|ない（受けた予約を台帳に記録）', 'y|できる', 'n|ない'),
        ('オンライン決済・回数券', 'n|ない', 'y|ある', 'n|ない'),
        ('トレーニングの記録', 'y|業種ごとの入力欄（重量×回数・マシン・ポーズなど）', '製品による', '書き方を自分で決める'),
        ('カウンセリング・同意書', 'y|iPad で記録・署名して PDF に', '製品による', '紙で保管'),
        ('スタッフで共有', 'y|招待した人だけ（日本・使う人ごとに購入）', 'y|できる', '紙は1冊、表計算はファイルの共有で'),
        ('データの置き場所', '端末とオーナーの iCloud', '提供会社のサーバー', '店舗の棚・パソコン'),
        ('ブラウザ・Android', 'n|使えない', 'y|使える', 'y|使える'),
    ],
    compare_note='予約・会員管理のシステムの内容は一般的な傾向です。料金や機能は各社の公式サイトで確かめてください。予約と決済はそうしたシステム、カルテと記録は KATACHI + と分けて使う店舗もあります。詳しくは<a href="./journal/trainer-kokyaku-kanri-app-erabikata.html">パーソナルトレーナーの顧客管理アプリの選び方と比較</a>・<a href="./journal/pilates-studio-kokyaku-kanri-erabikata.html">ピラティススタジオの顧客管理・予約システムの選び方と比較</a>へ。',
    where_intro='顧客の体や健康の情報は、預ける先が少ないほど安心です。KATACHI + は Pohoda のサーバーを使いません。',
    where=[
        ('端末', '記録は、まずこの iPhone・iPad・Mac に保存されます。Face ID やパスコードでアプリにロックをかけられます。'),
        ('オーナーの iCloud', '店舗のデータは、オーナーの Apple アカウントの iCloud に置かれ、招待したスタッフだけが読み書きできます。'),
        ('Pohoda のサーバー', 'ありません。記録は送られず、Pohoda が受け取ることも見ることもできません。'),
    ],
    where_note='共有には、オーナーとスタッフそれぞれの Apple アカウントと iCloud が必要で、店舗のデータはオーナーの iCloud 容量を使います。医療・診断を目的としたアプリではありません。詳しくは<a href="./legal/katachi-plus-privacy.html">プライバシーポリシー</a>へ。',
    steps_intro='営業の人との打ち合わせはありません。その日のうちに使い始められます。',
    steps=[
        ('店舗を作る', 'App Store から入れて、業種（筋トレ・ピラティス・ヨガ・ストレッチ）と店舗名を決めます。アカウント登録はありません。'),
        ('顧客を入れて記録する', '顧客を足して、カウンセリングとセッションを記録します。顧客5人までは無料で試せます。'),
        ('スタッフを招待する', '買い切りを購入して、店舗の設定の「スタッフを招待」から LINE やメールで招待を送ります。参加するスタッフもそれぞれ購入します。'),
    ],
    guide='katachi-plus-guide.html',
    faq=[
        ('KATACHI + はどんなサービスですか？', 'パーソナルトレーナーと小さなジム・スタジオのための、顧客カルテとトレーニング記録のサービスです。顧客台帳、カウンセリングシート、セッションの記録、予約台帳、分析、同意書への署名までをひとつにまとめ、同じ店舗のスタッフ全員で見て記録できます。iPhone・iPad・Mac のアプリで使います。'),
        ('料金はいくらですか？', '1人で使う分は無料で、自分の店舗1つで顧客5人まで記録できます。顧客を6人以上記録する、スタッフを招待して店舗で共有するときは、使う人それぞれが買い切り（980円）を一度だけ購入します。トレーナー3人の店舗なら合計2,940円で、以後の支払いはありません。'),
        ('顧客の記録はどこに保存されますか？', '端末と、オーナーの iCloud にだけ保存されます。Pohoda はサーバーを持たず、記録を受け取ることも見ることもできません。Face ID やパスコードでアプリにロックをかけられます。'),
        ('顧客が自分で予約できますか？', 'できません。予約台帳は、LINE や電話、外部の予約サービスで受けた予約を店舗側が記録するものです。顧客への通知もありません。店舗の予約ページのリンクを登録して、顧客に送ることはできます。'),
        ('お客さまの KATACHI とつなぐと、何が届きますか？', 'お客さまが個人用の KATACHI でつけた自主練の記録（筋トレの種目・重量・回数、有酸素の時間・速度・傾斜）が、カルテに届きます。送る項目はお客さまが選びます。体組成・体調・メモ・写真は届きません。店舗で記録したセッションとメニューをお客さまに見せるかは、店舗の設定で選べます。'),
        ('スタッフが辞めたら、記録はどうなりますか？', 'オーナーがその人を店舗から外すと、その人の端末から店舗の記録が消えます。オーナー側の記録は残ります。'),
        ('請求書払いはできますか？', 'できません。お支払いは App Store（Apple ID）だけです。領収書は Apple から届くメールか、App Store の購入履歴から出せます。'),
        ('対応機種と、利用の条件は？', 'iOS 18 以上の iPhone・iPad と、macOS 15 以上の Mac で使えます。ブラウザや Android では使えません。日本国内の事業者向けで、App Store の配信は日本だけです。医療・診断を目的としたアプリではありません。'),
    ],
    final_title='まずは顧客5人まで、無料で試せます',
    final_foot='運営は Pohoda（杉本 啓輔・個人事業）。日本の事業者向けです。',
    reads=[
        ('pilates-studio-kokyaku-kanri-erabikata.html', 'ピラティススタジオの顧客管理・予約システムの選び方と比較（2026）', '選び方'),
        ('trainer-kokyaku-kanri-app-erabikata.html', 'パーソナルトレーナーの顧客管理アプリの選び方と比較（2026）', '選び方'),
        ('personal-training-karte-template.html', 'パーソナルトレーニングのカルテ（テンプレート・印刷用・無料）', 'テンプレート'),
        ('personal-gym-counseling-sheet.html', 'パーソナルトレーニングのカウンセリングシート（パーソナルジム用）', 'テンプレート'),
    ],
)

PRODUCTS = {p['slug']: p for p in (ONE_CRM, KATACHI_PLUS)}


def cell(v):
    if v.startswith('y|'):
        return '<span class="yes"></span>' + v[2:]
    if v.startswith('n|'):
        return '<span class="no"></span>' + v[2:]
    return v


def img(src, w, h, alt, extra=''):
    return f'<img src="./assets/screens/{src}" alt="{alt}" width="{w}" height="{h}"{extra}>'


def render(p):
    url = f'https://pohoda.jp/{p["slug"]}.html'
    app = f'https://apps.apple.com/jp/app/id{p["app_id"]}?pt=128987033&amp;ct={p["ct"]}&amp;mt=8'
    pdf = f'./assets/{p["slug"]}-shiryo.pdf'
    og = f'https://pohoda.jp/assets/og/og-{p["slug"]}.png'
    pr = p['price']
    mail = f'mailto:{MAIL}?subject={p["name"].replace(" ", "%20").replace("+", "%2B")}%20%E3%81%AE%E5%95%8F%E3%81%84%E5%90%88%E3%82%8F%E3%81%9B'

    old = (ROOT / f'{p["slug"]}.html').read_text()
    header = old[old.index('<header class="site-header">'):old.index('</header>') + 9]
    footer = old[old.index('<footer class="site-footer">'):].replace('<script defer src="/carousel.js"></script>\n', '')

    pro_word = p['pro_name']
    offers = [{"@type": "Offer", "name": p['free_offer'], "price": "0", "priceCurrency": "JPY"},
              {"@type": "Offer", "name": f'{p["name"]} 買い切り（1人）', "price": str(pr['life']), "priceCurrency": "JPY"}]
    ld = [
        {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": p['name'], "operatingSystem": "iOS, iPadOS, macOS",
         "applicationCategory": "BusinessApplication", "url": url, "downloadUrl": f'https://apps.apple.com/jp/app/id{p["app_id"]}',
         "image": og, "description": p['ld_description'], "inLanguage": "ja", "offers": offers,
         "author": {"@type": "Organization", "name": "Pohoda", "url": "https://pohoda.jp/"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://pohoda.jp/"},
            {"@type": "ListItem", "position": 2, "name": "法人の方へ", "item": "https://pohoda.jp/business.html"},
            {"@type": "ListItem", "position": 3, "name": p['name'], "item": url}]},
    ]
    ldhtml = ''.join('<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(x, ensure_ascii=False) for x in ld)

    head = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p["title"]}</title>
<meta name="description" content="{p["description"]}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#fbfaf8">
<meta name="apple-itunes-app" content="app-id={p["app_id"]}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pohoda">
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="{p["og_title"]}">
<meta property="og:description" content="{p["og_description"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{p["og_title"]}">
<meta name="twitter:description" content="{p["og_description"]}">
<meta name="twitter:image" content="{og}">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="icon" href="/favicon-48.png?v=3" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=3">
<link rel="stylesheet" href="./styles.css?v=24">
<link rel="stylesheet" href="./assets/saas.css?v=2">
{ldhtml}</head>'''

    solve = ''.join(f'<div><span class="was">{w}</span><h3>{h}</h3><p>{t}</p></div>' for w, h, t in p['solve'])
    kinds = ''.join(f'<div><h3>{h}</h3><p class="who">{who}</p><p>{t}</p><p><a href="./journal/{href}">{lt}</a></p></div>'
                    for h, who, t, href, lt in p['kinds'])
    rows = ''
    for i, (h, t, items, shot) in enumerate(p['rows']):
        lis = ''.join(f'<li>{x}</li>' for x in items)
        rows += (f'\n    <div class="lp-row{" flip" if i % 2 else ""}">\n      <div><h3>{h}</h3><p>{t}</p><ul>{lis}</ul></div>\n      '
                 f'{img(*shot, extra=chr(32) + "loading=" + chr(34) + "lazy" + chr(34))}\n    </div>')
    more = ''.join(f'<li>{x}</li>' for x in p['more'])
    free_items = ''.join(f'<li>{x}</li>' for x in p['free_items'])
    pro_items = ''.join(f'<li>{x}</li>' for x in p['pro_items'])
    ctable = ''.join(f'<tr><th scope="row">{r[0]}</th>' + ''.join(f'<td>{cell(c)}</td>' for c in r[1:]) + '</tr>' for r in p['compare'])
    where = ''.join(f'<div{" class=" + chr(34) + "off" + chr(34) if i == 2 else ""}><h3>{h}</h3><p>{t}</p></div>' for i, (h, t) in enumerate(p['where']))
    steps = ''.join(f'<li><h3>{h}</h3><p>{t}</p></li>' for h, t in p['steps'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq'])
    reads = ''.join(f'<li><a href="./journal/{h}"><span>{t}</span><span>{tag}</span></a></li>' for h, t, tag in p['reads'])

    body = f'''
<body class="saas">

{header}

<nav class="lp-bar" aria-label="{p["name"]} のページ内">
  <div class="lp">
    <b><img src="./assets/{p["icon"]}" alt="" width="22" height="22">{p["name"]}</b>
    <a href="#features">機能</a><a href="#pricing">料金</a><a href="#compare">比較</a><a href="#security">安全性</a><a href="#faq">よくある質問</a><a href="{pdf}">資料</a>
    <a class="lp-btn lp-btn-main" href="{app}">無料ではじめる</a>
  </div>
</nav>

<main class="lp">
  <section class="lp-hero">
    <p class="lp-kind">{p["kind"]}</p>
    <h1>{p["h1"]}</h1>
    <p class="lp-lead">{p["lead"]}</p>
    <div class="lp-actions">
      <a class="lp-btn lp-btn-main" href="{app}">無料ではじめる</a>
      <a class="lp-btn lp-btn-sub" href="{pdf}">資料をダウンロード（PDF）</a>
    </div>
    <p class="lp-assure">{p["assure"]}</p>
    <figure class="lp-stage">
      {img(*p["hero_mac"], extra=' class="mac" fetchpriority="high"')}
      {img(*p["hero_phone"], extra=' class="phone"')}
    </figure>
  </section>

  <section class="lp-sec" aria-labelledby="h-solve">
    <div class="lp-head"><h2 class="lp-h2" id="h-solve">{p["solve_title"]}</h2></div>
    <div class="lp-three">{solve}</div>
  </section>

  <section class="lp-sec" aria-labelledby="h-kinds">
    <div class="lp-head"><h2 class="lp-h2" id="h-kinds">{p["kinds_title"]}</h2><p>{p["kinds_intro"]}</p></div>
    <div class="lp-kinds">{kinds}</div>
  </section>

  <section class="lp-sec" id="features" aria-labelledby="h-feats">
    <div class="lp-head"><h2 class="lp-h2" id="h-feats">機能</h2><p>{p["feats_intro"]}</p></div>{rows}
    <ul class="lp-more">{more}</ul>
  </section>

  <section class="lp-sec" id="pricing" aria-labelledby="h-pricing">
    <div class="lp-head"><h2 class="lp-h2" id="h-pricing">料金</h2><p>{p["pricing_intro"]}</p></div>
    <div class="lp-plans">
      <div class="lp-plan">
        <h3>{p["free_name"]}</h3>
        <div class="amount">¥0</div>
        <p class="sub">カードの登録なし</p>
        <a class="lp-btn lp-btn-sub" href="{app}">無料ではじめる</a>
        <ul>{free_items}</ul>
      </div>
      <div class="lp-plan is-pro">
        <h3>{pro_word}<span class="pro">1人あたり</span></h3>
        <div class="amount">{yen(pr["life"])}<small>一度だけ</small></div><p class="sub">{p["life_sub"]}</p>
        <a class="lp-btn lp-btn-main" href="{app}">{p["pro_btn"]}</a>
        <ul>{pro_items}</ul>
      </div>
    </div>
    <p class="lp-note">{p["price_note"]}</p>
  </section>

  <section class="lp-sec" id="compare" aria-labelledby="h-compare">
    <div class="lp-head"><h2 class="lp-h2" id="h-compare">ほかの方法との違い</h2><p>{p["compare_intro"]}</p></div>
    <div class="lp-scroll">
      <table class="lp-table lp-compare">
        <thead><tr><th scope="col"></th><th scope="col">{p["name"]}</th><th scope="col">{p["compare_cols"][0]}</th><th scope="col">{p["compare_cols"][1]}</th></tr></thead>
        <tbody>{ctable}</tbody>
      </table>
    </div>
    <p class="lp-note">{p["compare_note"]}</p>
  </section>

  <section class="lp-sec" id="security" aria-labelledby="h-where">
    <div class="lp-head"><h2 class="lp-h2" id="h-where">データの置き場所と安全性</h2><p>{p["where_intro"]}</p></div>
    <div class="lp-where">{where}</div>
    <p class="lp-note">{p["where_note"]}</p>
  </section>

  <section class="lp-sec" aria-labelledby="h-steps">
    <div class="lp-head"><h2 class="lp-h2" id="h-steps">導入の流れ</h2><p>{p["steps_intro"]}</p></div>
    <ol class="lp-steps">{steps}</ol>
    <p class="lp-note">画面ごとの手順は<a href="./{p["guide"]}">使い方ガイド</a>にあります。</p>
  </section>

  <section class="lp-sec" id="faq" aria-labelledby="h-faq">
    <div class="lp-head"><h2 class="lp-h2" id="h-faq">よくある質問</h2></div>
    <div class="lp-faq">{faq}</div>
  </section>

  <section class="lp-final" aria-labelledby="h-final">
    <h2 id="h-final">{p["final_title"]}</h2>
    <p>社内で回す資料は、料金・機能・データの置き場所を1枚の PDF にまとめています。入力なしで開けます。導入前の質問は <a href="{mail}">{MAIL}</a> へ。</p>
    <div class="lp-actions">
      <a class="lp-btn lp-btn-main" href="{app}">無料ではじめる</a>
      <a class="lp-btn lp-btn-sub" href="{pdf}">資料をダウンロード（PDF）</a>
    </div>
    <p class="lp-assure">{p["final_foot"]}</p>
  </section>

  <section class="lp-sec" aria-labelledby="h-reads">
    <div class="lp-head"><h2 class="lp-h2" id="h-reads">読みもの</h2></div>
    <ul class="lp-reads">{reads}</ul>
  </section>
</main>

'''
    return head + body + footer


SHEET_CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { width: 210mm; height: 297mm; padding: 13mm 14mm 11mm; font: 9pt/1.65 -apple-system, "Hiragino Sans", sans-serif;
       color: #5f5a52; background: #fbfaf8; -webkit-print-color-adjust: exact; print-color-adjust: exact; display: flex; flex-direction: column; }
h1, h2, h3, b { font-weight: 500; color: #1c1b19; }
.top { display: flex; justify-content: space-between; align-items: center; font-size: 8.5pt; }
.top span:first-child { display: flex; align-items: center; gap: 6px; color: #1c1b19; font-size: 10pt; }
.top img { width: 18px; height: 18px; border-radius: 5px; }
h1 { font-size: 21pt; line-height: 1.3; letter-spacing: -.02em; margin: 7mm 0 2.5mm; }
.lead { font-size: 9.5pt; max-width: 150mm; }
.shot { display: block; width: 100%; height: 62mm; object-fit: cover; object-position: top left; border: .3mm solid rgba(28,27,25,.16); border-radius: 3mm; margin: 5mm 0; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 7mm; }
h2 { font-size: 10.5pt; margin: 0 0 1.5mm; }
ul { list-style: none; }
li { position: relative; padding-left: 3.2mm; margin: 0 0 .6mm; }
li::before { content: ""; position: absolute; left: .4mm; top: .62em; width: 1.3mm; height: 1.3mm; border-radius: 50%; background: rgba(28,27,25,.25); }
table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: 1mm 1.5mm; border-bottom: .25mm solid rgba(28,27,25,.1); font-weight: 400; }
thead th { color: #8f897f; font-size: 8pt; }
tbody th, td { color: #1c1b19; }
.note { font-size: 7.5pt; color: #8f897f; margin-top: 1.2mm; }
.foot { margin-top: auto; padding-top: 4mm; border-top: .3mm solid rgba(28,27,25,.16); display: flex; justify-content: space-between; gap: 4mm; font-size: 8pt; white-space: nowrap; }
.foot b { font-size: 9.5pt; }
"""


def render_sheet(p):
    """資料 PDF（A4・1枚）の HTML。フォームなしで誰でも取れる、社内で回す用。"""
    pr = p['price']
    mac = p['hero_mac']
    feats = ''.join(f'<li>{h}</li>' for h, *_ in p['rows']) + ''.join(
        f'<li>{x.split("<span")[0]}</li>' for x in p['more'][:4])
    solve = ''.join(f'<li><b>{h}</b> {t.split("。")[0]}。</li>' for _, h, t in p['solve'])
    prow = ''.join(f'<tr><th>{n}人</th><td>{yen(pr["life"] * n)}</td><td>以後の支払いなし</td></tr>' for n in (1, 3, 5))
    where = ''.join(f'<li><b>{h}</b> {t.split("。")[0]}。</li>' for h, t in p['where'])
    steps = ''.join(f'<li><b>{i}. {h}</b> {t.split("。")[0]}。</li>' for i, (h, t) in enumerate(p['steps'], 1))
    return f"""<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>{p['name']} 資料</title><style>{SHEET_CSS}</style></head><body>
<div class="top"><span><img src="{ROOT}/assets/{p['icon']}" alt="">{p['name']}</span><span>{p['kind']}</span></div>
<h1>{p['h1'].replace('<br>', '')}</h1>
<p class="lead">{p['lead']}</p>
<img class="shot" src="{ROOT}/assets/screens/{mac[0]}" alt="">
<div class="grid">
  <div><h2>片づくこと</h2><ul>{solve}</ul></div>
  <div><h2>料金（税込・買い切りだけ）</h2>
    <table><thead><tr><th>使う人</th><th>買い切り（合計）</th><th></th></tr></thead><tbody>{prow}</tbody></table>
    <p class="note">{p['assure'].split('・カード')[0]}（カードの登録なし）。お支払いは App Store（Apple ID）。請求書払いはありません。</p></div>
  <div><h2>主な機能</h2><ul>{feats}</ul></div>
  <div><h2>データの置き場所</h2><ul>{where}</ul></div>
  <div><h2>導入の流れ</h2><ul>{steps}</ul></div>
  <div><h2>使える端末</h2><ul><li>iPhone・iPad・Mac（App Store・日本）</li><li>ブラウザ・Android・Windows では使えません</li></ul></div>
</div>
<div class="foot"><span><b>pohoda.jp/{p['slug']}.html</b>　App Store で「{p['name']}」</span><span>問い合わせ {MAIL}　運営 Pohoda（杉本 啓輔）</span></div>
</body></html>"""


CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

if __name__ == '__main__':
    import subprocess
    import tempfile
    for slug in sys.argv[1:] or PRODUCTS:
        p = PRODUCTS[slug]
        (ROOT / f'{slug}.html').write_text(render(p))
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
            f.write(render_sheet(p))
        out = ROOT / 'assets' / f'{slug}-shiryo.pdf'  # assets/docs は .assetsignore の docs で配信されない
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                        f'--print-to-pdf={out}', f'file://{f.name}'], check=True, capture_output=True)
        print('wrote', slug, out.relative_to(ROOT))
