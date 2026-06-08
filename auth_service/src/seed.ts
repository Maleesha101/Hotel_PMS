import { prisma } from './config/prisma';
import bcrypt from 'bcryptjs';
import { env } from './config/env';
import { Role } from './shared/enums';

const seedUsers = [
  {
    name: env.ADMIN_SEED_NAME,
    email: env.ADMIN_SEED_EMAIL,
    password: env.ADMIN_SEED_PASSWORD,
    role: Role.ADMIN,
    department: 'Management',
    employeeId: 'EMP-001',
  },
  {
    name: 'Sarah Front Desk',
    email: 'frontdesk@hotelpms.com',
    password: 'FrontDesk@1234',
    role: Role.FRONT_DESK,
    department: 'Reception',
    employeeId: 'EMP-002',
  },
  {
    name: 'Kumar Housekeeping',
    email: 'housekeeping@hotelpms.com',
    password: 'Housekeep@1234',
    role: Role.HOUSEKEEPING,
    department: 'Housekeeping',
    employeeId: 'EMP-003',
  },
  {
    name: 'Nimal Maintenance',
    email: 'maintenance@hotelpms.com',
    password: 'Maintain@1234',
    role: Role.MAINTENANCE,
    department: 'Maintenance',
    employeeId: 'EMP-004',
  },
  {
    name: 'Priya Accountant',
    email: 'accountant@hotelpms.com',
    password: 'Account@1234',
    role: Role.ACCOUNTANT,
    department: 'Finance',
    employeeId: 'EMP-005',
  },
];

(async () => {
  try {
    const count = await prisma.user.count();
    if (count > 0) {
      console.log('🚀 Users already exist, skipping seeding');
      process.exit(0);
    }
    for (const u of seedUsers) {
      const hash = await bcrypt.hash(u.password, env.BCRYPT_ROUNDS);
      await prisma.user.create({
        data: {
          name: u.name,
          email: u.email,
          passwordHash: hash,
          role: u.role,
          department: u.department,
          employeeId: u.employeeId,
        },
      });
    }
    console.log('✅ Seeded users');
  } catch (err) {
    console.error('❌ Seed error', err);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
})();
