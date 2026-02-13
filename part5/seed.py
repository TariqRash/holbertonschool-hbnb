"""
HBnB V2 — Database Seed Data
Saudi cities, property types, amenities, and sample places.
"""

from app import create_app, db
from app.models.user import User
from app.models.city import City
from app.models.place import PropertyType, Place
from app.models.amenity import Amenity


def seed():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding database...")

        # ── Admin user ──
        admin = User.query.filter_by(email='admin@hbnb.sa').first()
        if not admin:
            admin = User(
                first_name='Admin',
                last_name='HBnB',
                email='admin@hbnb.sa',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("  ✅ Admin user created")

        # ── Owner user ──
        owner = User.query.filter_by(email='owner@hbnb.sa').first()
        if not owner:
            owner = User(
                first_name='طارق',
                last_name='المطيري',
                email='owner@hbnb.sa',
                role='owner',
                is_active=True,
                preferred_language='ar'
            )
            owner.set_password('owner123')
            db.session.add(owner)
            print("  ✅ Owner user created")

        db.session.flush()

        # ── Cities ──
        cities_data = [
            {'name_en': 'Riyadh', 'name_ar': 'الرياض', 'region_en': 'Riyadh', 'region_ar': 'الرياض', 'latitude': 24.7136, 'longitude': 46.6753, 'is_featured': True, 'sort_order': 1},
            {'name_en': 'Jeddah', 'name_ar': 'جدة', 'region_en': 'Makkah', 'region_ar': 'مكة المكرمة', 'latitude': 21.5433, 'longitude': 39.1728, 'is_featured': True, 'sort_order': 2},
            {'name_en': 'Makkah', 'name_ar': 'مكة المكرمة', 'region_en': 'Makkah', 'region_ar': 'مكة المكرمة', 'latitude': 21.4225, 'longitude': 39.8262, 'is_featured': True, 'sort_order': 3},
            {'name_en': 'Madinah', 'name_ar': 'المدينة المنورة', 'region_en': 'Madinah', 'region_ar': 'المدينة المنورة', 'latitude': 24.5247, 'longitude': 39.5692, 'is_featured': True, 'sort_order': 4},
            {'name_en': 'Dammam', 'name_ar': 'الدمام', 'region_en': 'Eastern', 'region_ar': 'المنطقة الشرقية', 'latitude': 26.4207, 'longitude': 50.0888, 'is_featured': True, 'sort_order': 5},
            {'name_en': 'Abha', 'name_ar': 'أبها', 'region_en': 'Asir', 'region_ar': 'عسير', 'latitude': 18.2164, 'longitude': 42.5053, 'is_featured': True, 'sort_order': 6},
            {'name_en': 'Taif', 'name_ar': 'الطائف', 'region_en': 'Makkah', 'region_ar': 'مكة المكرمة', 'latitude': 21.2703, 'longitude': 40.4159, 'is_featured': False, 'sort_order': 7},
            {'name_en': 'Tabuk', 'name_ar': 'تبوك', 'region_en': 'Tabuk', 'region_ar': 'تبوك', 'latitude': 28.3838, 'longitude': 36.5550, 'is_featured': False, 'sort_order': 8},
            {'name_en': 'Al Khobar', 'name_ar': 'الخبر', 'region_en': 'Eastern', 'region_ar': 'المنطقة الشرقية', 'latitude': 26.2172, 'longitude': 50.1971, 'is_featured': False, 'sort_order': 9},
            {'name_en': 'Al Ula', 'name_ar': 'العلا', 'region_en': 'Madinah', 'region_ar': 'المدينة المنورة', 'latitude': 26.6173, 'longitude': 37.9216, 'is_featured': False, 'sort_order': 10},
        ]

        cities = {}
        for cd in cities_data:
            c = City.query.filter_by(name_en=cd['name_en']).first()
            if not c:
                c = City(**cd)
                db.session.add(c)
            cities[cd['name_en']] = c

        db.session.flush()
        print(f"  ✅ {len(cities)} cities seeded")

        # ── Property Types ──
        types_data = [
            {'name_en': 'Apartments', 'name_ar': 'شقق', 'icon': '🏢', 'sort_order': 1},
            {'name_en': 'Chalets', 'name_ar': 'شاليهات', 'icon': '🏠', 'sort_order': 2},
            {'name_en': 'Studios', 'name_ar': 'استديوهات', 'icon': '🏬', 'sort_order': 3},
            {'name_en': 'Retreats', 'name_ar': 'استراحات', 'icon': '⛱️', 'sort_order': 4},
            {'name_en': 'Resorts', 'name_ar': 'منتجعات', 'icon': '🏖️', 'sort_order': 5},
            {'name_en': 'Villas', 'name_ar': 'فلل', 'icon': '🏡', 'sort_order': 6},
            {'name_en': 'Farms', 'name_ar': 'مزارع', 'icon': '🌾', 'sort_order': 7},
            {'name_en': 'Camps', 'name_ar': 'مخيمات', 'icon': '⛺', 'sort_order': 8},
        ]

        prop_types = {}
        for td in types_data:
            pt = PropertyType.query.filter_by(name_en=td['name_en']).first()
            if not pt:
                pt = PropertyType(**td)
                db.session.add(pt)
            prop_types[td['name_en']] = pt

        db.session.flush()
        print(f"  ✅ {len(prop_types)} property types seeded")

        # ── Amenities ──
        amenities_data = [
            {'name_en': 'WiFi', 'name_ar': 'واي فاي', 'icon': 'wifi', 'category': 'essentials'},
            {'name_en': 'Air Conditioning', 'name_ar': 'تكييف', 'icon': 'thermometer-snowflake', 'category': 'essentials'},
            {'name_en': 'Parking', 'name_ar': 'موقف سيارات', 'icon': 'car', 'category': 'essentials'},
            {'name_en': 'Swimming Pool', 'name_ar': 'مسبح', 'icon': 'waves', 'category': 'leisure'},
            {'name_en': 'Kitchen', 'name_ar': 'مطبخ', 'icon': 'cooking-pot', 'category': 'essentials'},
            {'name_en': 'Washing Machine', 'name_ar': 'غسالة', 'icon': 'shirt', 'category': 'essentials'},
            {'name_en': 'TV', 'name_ar': 'تلفزيون', 'icon': 'tv', 'category': 'entertainment'},
            {'name_en': 'BBQ Grill', 'name_ar': 'شواية', 'icon': 'flame', 'category': 'outdoor'},
            {'name_en': 'Garden', 'name_ar': 'حديقة', 'icon': 'trees', 'category': 'outdoor'},
            {'name_en': 'Gym', 'name_ar': 'نادي رياضي', 'icon': 'dumbbell', 'category': 'leisure'},
            {'name_en': 'Elevator', 'name_ar': 'مصعد', 'icon': 'arrow-up-down', 'category': 'accessibility'},
            {'name_en': 'Security', 'name_ar': 'أمن', 'icon': 'shield-check', 'category': 'safety'},
            {'name_en': 'Hot Tub', 'name_ar': 'جاكوزي', 'icon': 'bath', 'category': 'leisure'},
            {'name_en': 'Fireplace', 'name_ar': 'مدفأة', 'icon': 'flame-kindling', 'category': 'comfort'},
            {'name_en': 'Workspace', 'name_ar': 'مكتب عمل', 'icon': 'laptop', 'category': 'business'},
        ]

        amenities = {}
        for i, ad in enumerate(amenities_data):
            a = Amenity.query.filter_by(name_en=ad['name_en']).first()
            if not a:
                a = Amenity(**ad, sort_order=i + 1)
                db.session.add(a)
            amenities[ad['name_en']] = a

        db.session.flush()
        print(f"  ✅ {len(amenities)} amenities seeded")

        # ── Sample Places ──
        places_data = [
            {
                'title_ar': 'شقة فاخرة وسط الرياض',
                'title_en': 'Luxury Apartment in Central Riyadh',
                'description_ar': 'شقة مفروشة بالكامل في قلب الرياض، قريبة من جميع الخدمات والمطاعم.',
                'description_en': 'Fully furnished apartment in the heart of Riyadh, close to all services and restaurants.',
                'price_per_night': 350,
                'city': 'Riyadh',
                'type': 'Apartments',
                'bedrooms': 2, 'bathrooms': 2, 'max_guests': 4, 'beds': 3,
                'trip_type': 'both',
                'is_featured': True,
                'latitude': 24.7136, 'longitude': 46.6753,
                'amenities': ['WiFi', 'Air Conditioning', 'Parking', 'Kitchen', 'TV', 'Workspace'],
            },
            {
                'title_ar': 'شاليه على البحر في جدة',
                'title_en': 'Beachfront Chalet in Jeddah',
                'description_ar': 'شاليه مميز على شاطئ البحر الأحمر مع مسبح خاص وإطلالة خلابة.',
                'description_en': 'Premium beachfront chalet on the Red Sea with private pool and stunning views.',
                'price_per_night': 800,
                'city': 'Jeddah',
                'type': 'Chalets',
                'bedrooms': 3, 'bathrooms': 3, 'max_guests': 8, 'beds': 5,
                'trip_type': 'family',
                'is_featured': True,
                'latitude': 21.5433, 'longitude': 39.1728,
                'amenities': ['WiFi', 'Air Conditioning', 'Parking', 'Swimming Pool', 'Kitchen', 'BBQ Grill', 'Garden'],
            },
            {
                'title_ar': 'استديو حديث في الدمام',
                'title_en': 'Modern Studio in Dammam',
                'description_ar': 'استديو عصري ومريح مثالي لرجال الأعمال والمسافرين الفرديين.',
                'description_en': 'Modern and comfortable studio ideal for business travelers and solo visitors.',
                'price_per_night': 180,
                'city': 'Dammam',
                'type': 'Studios',
                'bedrooms': 1, 'bathrooms': 1, 'max_guests': 2, 'beds': 1,
                'trip_type': 'business',
                'is_featured': False,
                'latitude': 26.4207, 'longitude': 50.0888,
                'amenities': ['WiFi', 'Air Conditioning', 'Parking', 'Kitchen', 'TV', 'Workspace', 'Gym'],
            },
            {
                'title_ar': 'فيلا فاخرة في أبها',
                'title_en': 'Luxury Villa in Abha',
                'description_ar': 'فيلا واسعة محاطة بالطبيعة الخلابة في أبها مع حديقة ومسبح.',
                'description_en': 'Spacious villa surrounded by beautiful nature in Abha with garden and pool.',
                'price_per_night': 1200,
                'city': 'Abha',
                'type': 'Villas',
                'bedrooms': 5, 'bathrooms': 4, 'max_guests': 12, 'beds': 7,
                'trip_type': 'family',
                'is_featured': True,
                'latitude': 18.2164, 'longitude': 42.5053,
                'amenities': ['WiFi', 'Air Conditioning', 'Parking', 'Swimming Pool', 'Kitchen', 'BBQ Grill', 'Garden', 'Security', 'Hot Tub'],
            },
            {
                'title_ar': 'استراحة عائلية في الطائف',
                'title_en': 'Family Retreat in Taif',
                'description_ar': 'استراحة مثالية للعائلات مع مسبح وحديقة ومنطقة شواء.',
                'description_en': 'Perfect family retreat with pool, garden, and BBQ area.',
                'price_per_night': 550,
                'city': 'Taif',
                'type': 'Retreats',
                'bedrooms': 3, 'bathrooms': 2, 'max_guests': 10, 'beds': 5,
                'trip_type': 'family',
                'is_featured': False,
                'latitude': 21.2703, 'longitude': 40.4159,
                'amenities': ['WiFi', 'Air Conditioning', 'Parking', 'Swimming Pool', 'Kitchen', 'BBQ Grill', 'Garden', 'Fireplace'],
            },
            {
                'title_ar': 'مخيم صحراوي في العلا',
                'title_en': 'Desert Camp in Al Ula',
                'description_ar': 'تجربة تخييم فريدة في صحراء العلا مع إطلالة على التكوينات الصخرية.',
                'description_en': 'Unique camping experience in Al Ula desert with views of rock formations.',
                'price_per_night': 400,
                'city': 'Al Ula',
                'type': 'Camps',
                'bedrooms': 1, 'bathrooms': 1, 'max_guests': 4, 'beds': 2,
                'trip_type': 'both',
                'is_featured': True,
                'latitude': 26.6173, 'longitude': 37.9216,
                'amenities': ['WiFi', 'BBQ Grill', 'Security'],
            },
            {
                'title_ar': 'منتجع ساحلي في الخبر',
                'title_en': 'Coastal Resort in Al Khobar',
                'description_ar': 'منتجع فاخر على الواجهة البحرية مع جميع وسائل الراحة.',
                'description_en': 'Luxury waterfront resort with all comfort amenities.',
                'price_per_night': 950,
                'city': 'Al Khobar',
                'type': 'Resorts',
                'bedrooms': 2, 'bathrooms': 2, 'max_guests': 6, 'beds': 3,
                'trip_type': 'both',
                'is_featured': True,
                'latitude': 26.2172, 'longitude': 50.1971,
                'amenities': ['WiFi', 'Air Conditioning', 'Parking', 'Swimming Pool', 'Kitchen', 'Gym', 'Hot Tub', 'Security'],
            },
            {
                'title_ar': 'مزرعة ريفية في تبوك',
                'title_en': 'Countryside Farm in Tabuk',
                'description_ar': 'مزرعة هادئة بعيداً عن صخب المدينة مع حيوانات وأشجار فاكهة.',
                'description_en': 'Peaceful farm away from city noise with animals and fruit trees.',
                'price_per_night': 300,
                'city': 'Tabuk',
                'type': 'Farms',
                'bedrooms': 2, 'bathrooms': 1, 'max_guests': 6, 'beds': 3,
                'trip_type': 'family',
                'is_featured': False,
                'latitude': 28.3838, 'longitude': 36.5550,
                'amenities': ['WiFi', 'Parking', 'Kitchen', 'BBQ Grill', 'Garden'],
            },
        ]

        for pd in places_data:
            existing = Place.query.filter_by(title_en=pd['title_en']).first()
            if existing:
                continue

            place = Place(
                title_ar=pd['title_ar'],
                title_en=pd['title_en'],
                description_ar=pd['description_ar'],
                description_en=pd['description_en'],
                price_per_night=pd['price_per_night'],
                city_id=cities[pd['city']].id,
                property_type_id=prop_types[pd['type']].id,
                owner_id=owner.id,
                bedrooms=pd['bedrooms'],
                bathrooms=pd['bathrooms'],
                max_guests=pd['max_guests'],
                beds=pd['beds'],
                trip_type=pd['trip_type'],
                is_featured=pd['is_featured'],
                latitude=pd['latitude'],
                longitude=pd['longitude'],
                is_active=True,
            )
            db.session.add(place)
            db.session.flush()

            # Add amenities
            for amenity_name in pd.get('amenities', []):
                if amenity_name in amenities:
                    place.amenities.append(amenities[amenity_name])

        db.session.commit()
        print(f"  ✅ {len(places_data)} sample places seeded")
        print("✅ Database seeding complete!")


if __name__ == '__main__':
    seed()
