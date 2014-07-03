# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.files import File
from domain.models import People, Topic, PeopleCategory, Statement, Meter
from account.models import Staff
from common.constants import STATUS_DRAFT, STATUS_PENDING, STATUS_PUBLISHED

from uuid import uuid1
import random

def randstr():
    return str(uuid1())[0: 10].replace('-', '')


def create_staff(username=None, email=None, password='password', first_name='', last_name='', occupation='', description='', homepage_url='', image='', is_staff=False):

    username = username or randstr()
    email = email or '%s@kmail.com' % username

    first_name = first_name or randstr()
    last_name = last_name or randstr()
    occupation = occupation or randstr()
    description = description or randstr()
    homepage_url = homepage_url or randstr()
    image = image or '%sdefault/default-people.png' % settings.FILES_WIDGET_TEMP_DIR


    staff = Staff.objects.create_user(
        username = username,
        email = email,
        password = password,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url,
        image = image
    )

    if is_staff:
        staff.is_staff = True
        staff.save()

    staff = Staff.objects.get(id=staff.id)

    return staff


def create_people_category(permalink=None, title='', description=''):

    permalink = permalink or randstr()
    title = title or randstr()
    description = description or randstr()

    people_category = PeopleCategory.objects.create(
        permalink = permalink,
        title = title,
        description = description
    )

    people_category = PeopleCategory.objects.get(id=people_category.id)

    return people_category


def create_people(permalink=None, first_name='', last_name='', occupation='', description='', homepage_url='', image='', category='', status=STATUS_PUBLISHED, created_by=''):

    created_by = created_by or create_staff()
    permalink = permalink or randstr()
    first_name = first_name or randstr()
    last_name = last_name or randstr()
    occupation = occupation or randstr()
    description = description or randstr()
    homepage_url = homepage_url or randstr()
    image = image or '%sdefault/default-people.png' % settings.FILES_WIDGET_TEMP_DIR
    category = category or create_people_category()

    people = People.objects.create(
        permalink = permalink,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url,
        image=image,
        status=status,
        created_by=created_by
    )
    people.categories.add(category)
    people.save()

    people = People.objects.get(id=people.id)


    return people


def create_topic(created_by=None, title='', description='', created=None, use_log_description=False):

    created_by = created_by or create_staff()
    title = title or randstr()

    long_description = '''
<h3>รถไฟความเร็วสูงของ ชัชชาติ</h3>
<p>จากการสัมภาษณ์ออกรายการเจาะข่าวตื้น ทาง ที่ออกอากาศเมื่อวันที่ 4 เมษายน 2557 ที่ผ่านมา นายชัชชาติ สิธิพันธุ์ รักษาการรัฐมนตรีว่าการกระทรวงคมนาคม ได้กล่าวเปรียบเทียบงบประมาณระว่างการสร้างรถไฟฟ้าในเขตกรุงเทพฯ และพื้นที่รอบนอกอีกส่วนหนึ่ง กับการสร้างรถไฟฟ้าความเร็วสูงที่ผ่านพื้นที่ 29 จังหวัด ไว้ว่า “…รถไฟ ในกรุงเทพฯ 4 แสนล้าน (งบประมาณการสร้างรถไฟฟ้า) แต่ 4 แสนล้านจังหวัดเดียว 7 แสนล้าน (งบประมาณในการสร้างรถไฟความเร็วสูง) นี่มัน 29 จังหวัด คนกรุงเทพฯก็จะชินกับรถไฟในกรุงเทพฯ แต่รถไฟความเร็วสูงคนค้านกันเยอะ”</p>
<h3>จากงบประมาณ 2 ล้านล้าน</h3>
<p>โครงการลงทุนโครงสร้างพื้นฐานวงเงิน 2 ล้านล้านบาท ที่มีกรอบระยะเวลาลงทุน 7 ปี (2557-2563) เป็นโครงการของรัฐบาลเพื่อพัฒนาโครงสร้างพื้นฐานด้านการคมนาคมของประเทศ เชื่อมต่อเส้นทางการเดินทางและขนส่ง ระหว่างภูมิภาคและประเทศใกล้เคียง ด้วยการขยายและพัฒนาระบบรถไฟความเร็วสูง และรถไฟรางคู่เป็นหลัก รวมถึงการลงทุนทางถนน และท่าเรือน้ำลึก</p>
<p>จากตัวโครงการทั้งหลายยังคงเป็นที่วิพากษ์วิจารณ์ถึงความคุ้มค่าของการลงทุน และมีกระแสคัดค้านจากหลายภาคส่วน เพราะไม่แน่ใจว่าจะเป็นตอบโจทย์การเสริมสร้างขีดความสามารถในการแข่งขัน ลดต้นทุนโลจิสติกส์ ต้นทุนการขนส่งสินค้าที่แท้จริงหรือไม่ และจากงบประมาณ 2 ล้านล้านตรงนี้ได้มีการแยกออกมาว่างบประมาณที่ใช้ในเรื่องระบบรางเป็นงบประมาณกว่า 80% ของงบประมาณทั้งหมด</p>
<h3>รถไฟฟ้า VS รถไฟความเร็วสูง </h3>
<p>เมื่อดูประกอบกับ เอกสารประกอบการพิจารณา ร่างพระราชบัญญัติให้อานาจกระทรวงการคลังกู้เงินเพื่อ การพัฒนาโครงสร้างพื้นฐานด้านคมนาคมขนส่งของประเทศ พ.ศ. … จะทำให้เห็นตัวเลขชัดเจนขึ้นว่าในส่วนของรถไฟความเร็วสูง อยู่ในแผนพัฒนาโครงข่ายเชื่อมต่อภูมิภาค มีตัวเลขงบประมาณอยู่ที่ 994,430.90 ล้านบาท โดย เป็นโครงการรถไฟความเร็วสูง 4 โครงการ เป็นโครงการรถไฟรางคู่ 2 โครงการ และโครงการสร้างทางหลวงพิเศษ 3 โครงการ วงเงินสำหรับรถไฟความเร็วสูงทั้งหมดคิดเป็น 783,229.9 ล้านบาท ส่วนงบประมาณในส่วนของการสร้างรถไฟฟ้า อยู่ในส่วนของแผนพัฒนาระบบขนส่งในเขตเมือง มีตัวเลขงบอยู่ที่ 472,448.12 ล้านบาท</p>
<p>และได้มีการสรุปสัดส่วนการใช้งบ 2 ล้านล้านออกมาในโลกออนไลน์ ว่ากามีการใช้งบในส่วน รถไฟความเร็วสูง 783,553 ล้านบาท คิดเป็น 39.2%  รถไฟฟ้า 456,662 ล้านบาท คิดเป็น 22.8%</p>
<p>ถนนทางหลวง 241,080 ล้านบาท คิดเป็น 12.1%  ถนนทางหลวงชนบท 34,309 ล้านบาท คิดเป็น 1.7%  สถานีขนส่งสินค้า 14,093 ล้านบาท คิดเป็น 0.7%  ท่าเรือ 29,581 ล้านบาท คิดเป็น 1.5%  ด่านศุลกากร 12,545 ล้านบาท คิดเป็น 0.6%</p><p>ปรับปรุงระบบรถไฟ (เพิ่มเครื่องกั้น ซ่อมบำรุงรางที่เสียหาย) 23,236 ล้านบาท คิดเป็น 1.2%  รถไฟทางคู่ และทางคู่เส้นทางใหม่ 383,891 ล้านบาท คิดเป็น 19.2%  ค่าสำรองเผื่อฉุกเฉิน (ความผันผวนราคาวัสดุ การติดตามและประเมินผล) 21,050 ล้านบาท คิดเป็น 1.0% ซึ่งแม้ตัวเลขจะคลาดเคลื่อนจากในเอกสารประกอบร่างพระราชบัญญัติไปบ้าง แต่ก็มีความใกล้เคียง</p>
<p>ทั้งนี้ทั้งนั้นก่อนหน้านี้ในปี 2554 ได้มีตัวเลขประมาณการงบประมาณการสร้างรถไฟฟ้า 10 สายในเขตกรุงเทพว่ารวมๆ แล้วจะต้องใช้งบลงทุนประมาณ 668,593 ล้านบาท (รวมค่าเวนคืน-ก่อสร้าง-งานระบบ)</p>
'''
    if use_log_description:
        description = description or '%s %s' % (long_description, randstr())
    else:
        description = description or randstr()

    topic = Topic.objects.create(
        title  = title,
        description = description,
        created_by = created_by
    )

    topic = Topic.objects.get(id=topic.id)

    return topic


def create_meter(permalink=None, title='', description='', point=0, order=0, image_large_text='', image_medium_text='', image_small_text='', image_small=''):

    permalink = permalink or randstr()
    title = title or randstr()
    description = description or randstr()


    image_large_text = image_large_text or '%sdefault_meters/status-unverifiable---large-text.png' % settings.FILES_WIDGET_TEMP_DIR
    image_medium_text = image_medium_text or '%sdefault_meters/status-unverifiable---medium-text.png' % settings.FILES_WIDGET_TEMP_DIR
    image_small_text = image_small_text or '%sdefault_meters/status-unverifiable---small-text.png' % settings.FILES_WIDGET_TEMP_DIR
    image_small = image_small or '%sdefault_meters/status-unverifiable---small.png' % settings.FILES_WIDGET_TEMP_DIR



    meter = Meter.objects.create(
        permalink=permalink,
        title=title,
        description=description,
        point=point,
        order=order,
        image_large_text=image_large_text,
        image_small_text=image_small_text,
        image_medium_text=image_medium_text,
        image_small=image_small
    )

    meter = Meter.objects.get(id=meter.id)

    return meter


def create_statement(created_by=None, quoted_by=None, permalink=None, quote='', references=None, status=STATUS_PENDING, topic=None, tags='hello world', meter=None, relate_statements=[], relate_peoples=[], published=None, published_by=None, source='', created=None, created_raw=None, changed=None, use_log_description=False, hilight=False, promote=False):

    created_by_list = list(Staff.objects.all()) or [None]
    created_by = created_by or random.choice(created_by_list) or create_staff()

    quoted_by_list = list(People.objects.all()) or [None]
    quoted_by = quoted_by or random.choice(quoted_by_list) or create_people()


    meter_list = list(Meter.objects.all()) or [None]
    meter = meter or random.choice(meter_list) or create_meter()

    topic = topic or create_topic(created_by=created_by, use_log_description=use_log_description)

    permalink = permalink or randstr()

    dummy_text = u'ฮิแฟ็กซ์ อมาตยาธิปไตยอีโรติก สหรัฐแก๊สโซฮอล์ สหรัฐบอเอ็กซ์เพรสคาแร็คเตอร์ชะโป่าไม้สระโงกอ่อนด้อยเทอร์โบบ็อกซ์ ฟลุกแทงโก้สะกอม ฮิแฟ็กซ์ อมาตยาธิปไตยอีโรติก สหรัฐแก๊สโซฮอล์ สหรัฐบอเอ็กซ์เพรสคาแร็คเตอร์ชะโป่าไม้สระโงกอ่อนด้อยเทอร์โบบ็อกซ์ ฟลุกแทงโก้สะกอม ฮิแฟ็กซ์'

    quote = quote or '%s %s' % (dummy_text, randstr())
    source = source or randstr()
    references = references or [{'url': 'http://%s.com/' % randstr(), 'title': randstr()}, {'url': 'http://%s.com/' % randstr(), 'title': randstr()}]
    statement = Statement.objects.create(
        permalink=permalink,
        quote=quote,
        references=references,
        status=status,
        quoted_by=quoted_by,
        created_by=created_by,
        topic=topic,
        tags=tags,
        meter=meter,
        published=published,
        published_by=published_by,
        source=source,
        created=created,
        created_raw=created_raw,
        changed=changed,
        hilight=hilight,
        promote=promote
    )

    for relate_statement in relate_statements:
        statement.relate_statements.add(relate_statement)

    for relate_people in relate_peoples:
        statement.relate_peoples.add(relate_people)

    statement = Statement.objects.get(id=statement.id)

    return statement